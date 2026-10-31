import sys
sys.path.insert(0, "backend")

from app.html_model import model, FEATURE_NAMES

booster = model.get_booster()
model_names = booster.feature_names

print("Extractor feature count:", len(FEATURE_NAMES))
print("Model feature count:", booster.num_features())
print("Model stores feature names:", model_names is not None)

if model_names:
    print("Stored names match extractor order:", model_names == FEATURE_NAMES)

    if model_names != FEATURE_NAMES:
        print("\nFirst mismatches:")
        for i, (extractor_name, model_name) in enumerate(
            zip(FEATURE_NAMES, model_names)
        ):
            if extractor_name != model_name:
                print(
                    f"Index {i}: extractor={extractor_name!r}, "
                    f"model={model_name!r}"
                )
                if i >= 20:
                    break

print("\nFirst 15 extractor names:")
for i, name in enumerate(FEATURE_NAMES[:15]):
    print(i, name)

if model_names:
    print("\nFirst 15 model names:")
    for i, name in enumerate(model_names[:15]):
        print(i, name)
