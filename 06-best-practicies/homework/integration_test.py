import os
from batch import get_input_path, get_output_path
from tests.test_batch import prepare_input_data
import pandas as pd

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}

df_input, _ = prepare_input_data()

df_input.to_parquet(
    get_input_path(2023,1),
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

os.system("aws --endpoint-url=http://localhost:4566 s3 ls --summarize --recursive s3://nyc-duration/in")  

os.system("python batch.py 2023 1")

os.system("aws --endpoint-url=http://localhost:4566 s3 ls --summarize --recursive s3://nyc-duration/out") 

df = pd.read_parquet(get_output_path(2023,1),
                storage_options=options)

print(df)
print(f"Sum of predicted durations {df['predicted_duration'].sum():.2f}")