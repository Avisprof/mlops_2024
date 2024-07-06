import os
from src.batch import get_input_path
from tests.test_batch import prepare_input_data

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

os.system("aws --endpoint-url=http://localhost:4566 s3 ls")  