import sys
sys.path.insert(0, "backend")

from app.inference import phishalign_model, PHISHALIGN_FEATURES

print("Model type:", type(phishalign_model).__name__)
print("Expected input features:", len(PHISHALIGN_FEATURES))

if hasattr(phishalign_model, "named_steps"):
    print("\nPipeline steps:")
    for name, step in phishalign_model.named_steps.items():
        print(f"  {name}: {type(step).__name__}")

    final_estimator = list(phishalign_model.named_steps.values())[-1]
else:
    final_estimator = phishalign_model

if hasattr(final_estimator, "coef_"):
    print("\nFeature coefficients:")
    coefficients = final_estimator.coef_[0]

    for name, value in sorted(
        zip(PHISHALIGN_FEATURES, coefficients),
        key=lambda item: abs(float(item[1])),
        reverse=True,
    ):
        print(f"{name}: {float(value):+.6f}")
else:
    print("\nNo direct coef_ found on final estimator.")
    print("Estimator attributes:", type(final_estimator).__name__)
