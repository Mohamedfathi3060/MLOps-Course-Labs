"""
Tests for the Churn Prediction API.
"""

from litestar.testing import TestClient
from main import app
from app.model_utils import predict_churn


def test_predict_churn_returns_valid_prediction():
    sample_features = [
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
    result = predict_churn(sample_features)
    assert result in [0, 1]


def test_predict_churn_edge_cases():
    zero_features = [0.0] * 11
    assert predict_churn(zero_features) in [0, 1]

    ones_features = [1.0] * 11
    assert predict_churn(ones_features) in [0, 1]

    large_features = [
        1000.0,
        100.0,
        50.0,
        5000.0,
        3.0,
        1.0,
        1.0,
        500000.0,
        1.0,
        0.0,
        0.0,
    ]
    assert predict_churn(large_features) in [0, 1]


def test_post_predict_endpoint():
    with TestClient(app=app) as client:
        payload = {
            "CreditScore": -1.6532555978100791,
            "Age": -0.47907533347697956,
            "Tenure": -1.3559114022278245,
            "Balance": -1.3559114022278245,
            "NumOfProducts": -1.3559114022278245,
            "HasCrCard": -1.3559114022278245,
            "IsActiveMember": -1.3559114022278245,
            "EstimatedSalary": -1.3559114022278245,
            "Geography_Germany": 1,
            "Geography_Spain": 0,
            "Gender_Male": 0,
        }

        response = client.post("/predict", json=payload)

        assert response.status_code == 201
        data = response.json()

        assert "prediction" in data
        assert data["prediction"] in [0, 1]


def test_get_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


def test_get_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "Hello, world!" in response.text


def test_post_predict_invalid_input():
    with TestClient(app=app) as client:
        invalid_payload = {
            "CreditScore": -1.6532555978100791,
            "Age": -0.47907533347697956,
            "Tenure": -1.3559114022278245,
            "Balance": -1.3559114022278245,
        }

        response = client.post("/predict", json=invalid_payload)
        assert response.status_code == 400
