## How to reproduce the project

1. Install packages with `pipenv`:
<br>`pip install pipenv`
<br>`pipenv install`

2. Run the MLflow UI locally:
<br>`mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns`

3. Open in the browser:
<br>`http://127.0.0.1:5000/`</br>

4. Run the hyperopt tuning:
<br>`pipenv run python src/train_hyperopt.py`<br>

5. Register the best model and get `RUN_ID`:
<br>`pipenv run python src/register_model.py`</br>

6. Set the environment `RUN_ID`:
<br>`export RUN_ID=97127fd0259844928e9ee35f81711439`</br>

7. Run the test:
<br>`pipenv run pytest tests/`</br>