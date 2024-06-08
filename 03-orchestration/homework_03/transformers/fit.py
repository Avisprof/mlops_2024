from typing import Tuple
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer



@transformer
def transform(df: pd.DataFrame, **kwargs) -> Tuple[BaseEstimator, BaseEstimator]:

    cat_columns = ['PULocationID', 'DOLocationID']
    df_dict = df[cat_columns].astype(str).to_dict(orient='records')

    enc = DictVectorizer(sparse=True)
    X = enc.fit_transform(df_dict)
    y = df['duration']

    model = LinearRegression()
    model.fit(X, y)

    print(f"intercept: {model.intercept_:.2f}")

    return model, enc   
    