from typing import Tuple
from sklearn.base import BaseEstimator
import mlflow
import pickle


mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("ny_yellow_taxi_data")

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data(data: Tuple[BaseEstimator, BaseEstimator]) -> Tuple[BaseEstimator, BaseEstimator]:

    model  = data[0]
    enc = data[1]
    enc_path = "mlflow/dv.vect" 

    with open(enc_path, "wb") as f_out:
        pickle.dump(enc, f_out)

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "models")
        mlflow.log_artifact(local_path=enc_path, artifact_path="models_pickle")

    return model, enc