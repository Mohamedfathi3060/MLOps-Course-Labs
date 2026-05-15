"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""

import pickle

with open("data/model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_churn(features: list[float]) -> int:
    prediction = model.predict([features])
    return int(prediction[0])


if __name__ == "__main__":
    sample = [
        -1.6532555978100791,
        -0.47907533347697956,
        -1.3559114022278245,
        0.9515606038935047,
        -0.7700253680702854,
        0.6490271882799827,
        -0.9370854375453458,
        1.6307585905747244,
        0.0,
        1.0,
        0.0,
    ]
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
