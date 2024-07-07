## How to reproduce the project

1. Install packages with `pipenv`:
```bash
pip install pipenv
pipenv install
```

2. Run the MLflow UI locally:
```bash   
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

3. Open in the browser:
```
http://127.0.0.1:5000/
```

4. Run the hyperopt tuning:
```bash
pipenv run python src/train_hyperopt.py
```

5. Register the best model and get `RUN_ID`:
```bash
pipenv run python src/register_model.py
```

6. Set the environment `RUN_ID`:
```bash
export RUN_ID=97127fd0259844928e9ee35f81711439
```

7. Run the test:
```bash
pipenv run pytest tests/
```
