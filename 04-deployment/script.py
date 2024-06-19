import os
import pickle
import pandas as pd

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename:str) -> pd.DataFrame:
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def predict(year:int, month:int) -> pd.Series:
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    print(f'Read URL: {url}')

    df = read_data(url)
    print(f'Data shape: {df.shape}')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    return y_pred

if __name__ == '__main__':
    year = int(os.environ.get("YEAR"))
    month = int(os.environ.get("MONTH"))
    y_pred = predict(year, month)
    print(f'y_pred: {y_pred.mean():.2f} +- {y_pred.std():.2f}')








