import pandas as pd
from datetime import datetime
from batch import prepare_data
from pandas.testing import assert_frame_equal

def prepare_input_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    return pd.DataFrame(data, columns=columns), columns


def test_prepare_data():

    df, columns = prepare_input_data()
    
    categorical = ['PULocationID', 'DOLocationID']
    actual_dataframe = prepare_data(df, categorical)

    expected_data = [
        ('-1', '-1', dt(1, 1), dt(1, 10), 9.0),
        ('1', '1', dt(1, 2), dt(1, 10), 8.0),
    ]
    expected_columns = columns + ['duration']
    expected_dataframe = pd.DataFrame(expected_data, columns=expected_columns)

    # compare dataframes
    assert_frame_equal(actual_dataframe, expected_dataframe)

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)