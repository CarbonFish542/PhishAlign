from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = (
    MODEL_DIR /
    "visual_validation_model_oofprotocol.pth"
)


# ============================================================
# Frozen research configuration
# ============================================================

IMAGE_SIZE = 224

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


# ============================================================
# Device
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# Exact research preprocessing
# ============================================================

image_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=MEAN,
        std=STD,
    ),
])


# ============================================================
# Exact research model architecture
# ============================================================

def build_model():
    """
    Recreate the exact MobileNetV3-Small architecture used
    during research.
    """

    # Architecture must match the research checkpoint.
    model = models.mobilenet_v3_small(
        weights=None
    )

    in_features = model.classifier[-1].in_features

    model.classifier[-1] = nn.Linear(
        in_features,
        2
    )

    return model


# ============================================================
# Load frozen checkpoint
# ============================================================

model = build_model()

state_dict = torch.load(
    MODEL_PATH,
    map_location=device,
)

model.load_state_dict(state_dict)

model = model.to(device)
model.eval()


# ============================================================
# Image loading
# ============================================================

def load_image(image_path):
    """
    Load and preprocess a screenshot exactly as the research
    pipeline did.
    """

    path = Path(str(image_path))

    if not path.is_file():
        raise FileNotFoundError(
            f"Screenshot not found: {path}"
        )

    with Image.open(path) as image:
        image = image.convert("RGB")
        tensor = image_transform(image)

    return tensor


# ============================================================
# Prediction from PIL image
# ============================================================

def predict_image(image):
    """
    Predict phishing probability from a PIL image.
    """

    image = image.convert("RGB")

    tensor = image_transform(image)
    tensor = tensor.unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(tensor)

        probability = torch.softmax(
            logits,
            dim=1,
        )[0, 1].item()

    return float(probability)


# ============================================================
# Prediction from screenshot path
# ============================================================

def predict_visual(image_path):
    """
    Predict phishing probability from a screenshot file.
    """

    path = Path(str(image_path))

    if not path.is_file():
        raise FileNotFoundError(
            f"Screenshot not found: {path}"
        )

    with Image.open(path) as image:
        return predict_image(image)