from src.model import ModelService

def test_prepare_features():

    model_service = ModelService(None)

    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    }

    expected_features = {
        "PU_DO": "130_205",
        "trip_distance": 3.66
    }

    actual_features = model_service.prepare_features(ride)

    assert actual_features == expected_features

class ModelMock:

    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():

    model = ModelMock(10.0)
    model_service = ModelService(model)

    features = {
        "PU_DO": "130_205",
        "trip_distance": 3.66
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction