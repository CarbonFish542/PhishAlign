from pathlib import Path
import json
import random
import time

import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

# -------------------- Configuration --------------------

ROOT = Path(r"D:\Phish360")
METADATA = ROOT / "metadata" / "phish360_metadata_split_clean.csv"
UNREADABLE = ROOT / "metadata" / "unreadable_screenshots.csv"
OUTPUT = ROOT / "visual_baseline_output"

SEED = 42
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 1e-4
PATIENCE = 3

# Label mapping: legitimate = 0, phishing = 1
LABEL_MAP = {"legitimate": 0, "phishing": 1}

# -------------------- Reproducibility --------------------

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

OUTPUT.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)
if device.type == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))

# -------------------- Load and filter metadata --------------------

if not METADATA.is_file():
    raise FileNotFoundError(f"Metadata not found: {METADATA}")

if not UNREADABLE.is_file():
    raise FileNotFoundError(f"Unreadable-image report not found: {UNREADABLE}")

df = pd.read_csv(METADATA)
bad_df = pd.read_csv(UNREADABLE)
excluded_ids = set(bad_df["sample_id"].astype(str))

# Explicitly use development splits only. The official test split
# and test_connected samples are not loaded by this script.
df = df[df["dataset_split"].isin(["train", "validation"])].copy()
df["sample_id"] = df["sample_id"].astype(str)
df = df[~df["sample_id"].isin(excluded_ids)].copy()

df["label"] = df["binary_label"].map(LABEL_MAP)
if df["label"].isna().any():
    raise ValueError("Unexpected or missing binary_label values found.")

df["label"] = df["label"].astype(int)
df["screenshot_path"] = df["screenshot_path"].astype(str)

missing_paths = df[~df["screenshot_path"].apply(lambda p: Path(p).is_file())]
if len(missing_paths):
    raise FileNotFoundError(
        f"{len(missing_paths)} screenshot paths do not exist. "
        "Review the metadata before training."
    )

train_df = df[df["dataset_split"] == "train"].reset_index(drop=True)
val_df = df[df["dataset_split"] == "validation"].reset_index(drop=True)

print("\nSamples after exclusions:")
print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Excluded unreadable screenshots:", len(excluded_ids))
print("\nTraining label counts:")
print(train_df["binary_label"].value_counts().to_string())
print("\nValidation label counts:")
print(val_df["binary_label"].value_counts().to_string())

# Save the exact sample IDs used for reproducibility.
pd.concat([
    train_df.assign(model_split="train"),
    val_df.assign(model_split="validation")
])[["sample_id", "model_split", "binary_label", "screenshot_path"]].to_csv(
    OUTPUT / "used_samples.csv", index=False
)

# -------------------- Image transforms --------------------

# Screenshots are resized to a consistent input size.
# No horizontal flips are used because they would reverse webpage text/logos.
train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

val_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

class ScreenshotDataset(Dataset):
    def __init__(self, frame, transform):
        self.frame = frame.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.frame)

    def __getitem__(self, index):
        row = self.frame.iloc[index]
        path = row["screenshot_path"]

        with Image.open(path) as image:
            image = image.convert("RGB")
            image_tensor = self.transform(image)

        label = int(row["label"])
        return image_tensor, label, row["sample_id"]

train_dataset = ScreenshotDataset(train_df, train_transform)
val_dataset = ScreenshotDataset(val_df, val_transform)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    pin_memory=(device.type == "cuda"),
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
    pin_memory=(device.type == "cuda"),
)

# -------------------- Model --------------------

print("\nLoading ImageNet-pretrained MobileNetV3-Small...")
weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# Replace the final classifier layer for two classes.
in_features = model.classifier[-1].in_features
model.classifier[-1] = nn.Linear(in_features, 2)
model = model.to(device)

# Inverse-frequency class weights, calculated from training data only.
counts = train_df["label"].value_counts().sort_index()
class_weights = torch.tensor(
    [len(train_df) / (2.0 * counts.loc[i]) for i in [0, 1]],
    dtype=torch.float32,
    device=device,
)

criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode="min", factor=0.5, patience=1
)

print("Class weights [legitimate, phishing]:", class_weights.tolist())

# -------------------- Training and validation --------------------

best_val_loss = float("inf")
epochs_without_improvement = 0
history = []
best_model_path = OUTPUT / "mobilenetv3_small_best.pth"

for epoch in range(1, EPOCHS + 1):
    start_time = time.time()

    model.train()
    train_loss_sum = 0.0
    train_correct = 0
    train_total = 0

    for images, labels, _ in train_loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        train_loss_sum += loss.item() * labels.size(0)
        train_correct += (logits.argmax(dim=1) == labels).sum().item()
        train_total += labels.size(0)

    train_loss = train_loss_sum / train_total
    train_accuracy = train_correct / train_total

    model.eval()
    val_loss_sum = 0.0
    val_total = 0
    all_labels = []
    all_predictions = []
    all_phishing_probabilities = []
    all_sample_ids = []

    with torch.no_grad():
        for images, labels, sample_ids in val_loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            logits = model(images)
            loss = criterion(logits, labels)
            probabilities = torch.softmax(logits, dim=1)
            predictions = logits.argmax(dim=1)

            val_loss_sum += loss.item() * labels.size(0)
            val_total += labels.size(0)

            all_labels.extend(labels.cpu().tolist())
            all_predictions.extend(predictions.cpu().tolist())
            all_phishing_probabilities.extend(probabilities[:, 1].cpu().tolist())
            all_sample_ids.extend(list(sample_ids))

    val_loss = val_loss_sum / val_total
    val_accuracy = accuracy_score(all_labels, all_predictions)
    scheduler.step(val_loss)

    elapsed = time.time() - start_time
    current_lr = optimizer.param_groups[0]["lr"]

    print(
        f"Epoch {epoch:02d}/{EPOCHS} | "
        f"train loss {train_loss:.4f} | "
        f"train acc {train_accuracy:.4f} | "
        f"val loss {val_loss:.4f} | "
        f"val acc {val_accuracy:.4f} | "
        f"lr {current_lr:.2e} | "
        f"{elapsed:.1f}s"
    )

    history.append({
        "epoch": epoch,
        "train_loss": train_loss,
        "train_accuracy": train_accuracy,
        "validation_loss": val_loss,
        "validation_accuracy": val_accuracy,
        "learning_rate": current_lr,
        "seconds": elapsed,
    })

    # Select the checkpoint using validation loss only.
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        epochs_without_improvement = 0
        torch.save(model.state_dict(), best_model_path)
        print("  Saved new best checkpoint.")
    else:
        epochs_without_improvement += 1

    if epochs_without_improvement >= PATIENCE:
        print(f"Early stopping: no validation-loss improvement for {PATIENCE} epochs.")
        break

# -------------------- Final validation evaluation --------------------

print("\nLoading best validation-loss checkpoint...")
model.load_state_dict(torch.load(best_model_path, map_location=device, weights_only=True))
model.eval()

all_labels = []
all_predictions = []
all_phishing_probabilities = []
all_sample_ids = []

with torch.no_grad():
    for images, labels, sample_ids in val_loader:
        images = images.to(device, non_blocking=True)
        logits = model(images)
        probabilities = torch.softmax(logits, dim=1)
        predictions = logits.argmax(dim=1)

        all_labels.extend(labels.tolist())
        all_predictions.extend(predictions.cpu().tolist())
        all_phishing_probabilities.extend(probabilities[:, 1].cpu().tolist())
        all_sample_ids.extend(list(sample_ids))

metrics = {
    "model": "MobileNetV3-Small",
    "pretrained_weights": "ImageNet DEFAULT",
    "image_size": IMAGE_SIZE,
    "batch_size": BATCH_SIZE,
    "epochs_configured": EPOCHS,
    "epochs_completed": len(history),
    "learning_rate": LEARNING_RATE,
    "seed": SEED,
    "device": str(device),
    "train_samples": len(train_df),
    "validation_samples": len(val_df),
    "excluded_unreadable_screenshots": len(excluded_ids),
    "accuracy": float(accuracy_score(all_labels, all_predictions)),
    "phishing_precision": float(precision_score(all_labels, all_predictions, pos_label=1, zero_division=0)),
    "phishing_recall": float(recall_score(all_labels, all_predictions, pos_label=1, zero_division=0)),
    "phishing_f1": float(f1_score(all_labels, all_predictions, pos_label=1, zero_division=0)),
    "roc_auc": float(roc_auc_score(all_labels, all_phishing_probabilities)),
    "confusion_matrix_labels_order": ["legitimate", "phishing"],
    "confusion_matrix": confusion_matrix(all_labels, all_predictions, labels=[0, 1]).tolist(),
    "classification_report": classification_report(
        all_labels,
        all_predictions,
        labels=[0, 1],
        target_names=["legitimate", "phishing"],
        output_dict=True,
        zero_division=0,
    ),
}

predictions_df = pd.DataFrame({
    "sample_id": all_sample_ids,
    "true_label": ["phishing" if x == 1 else "legitimate" for x in all_labels],
    "predicted_label": ["phishing" if x == 1 else "legitimate" for x in all_predictions],
    "phishing_probability": all_phishing_probabilities,
})
predictions_df.to_csv(OUTPUT / "validation_predictions.csv", index=False)

pd.DataFrame(history).to_csv(OUTPUT / "training_history.csv", index=False)

with open(OUTPUT / "validation_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("\nFinal validation metrics:")
for key in [
    "accuracy",
    "phishing_precision",
    "phishing_recall",
    "phishing_f1",
    "roc_auc",
]:
    print(f"{key}: {metrics[key]:.4f}")

print("\nConfusion matrix [ [TN, FP], [FN, TP] ]:")
print(np.array(metrics["confusion_matrix"]))

print("\nOutputs saved to:", OUTPUT)
print("Official test split was not used.")
