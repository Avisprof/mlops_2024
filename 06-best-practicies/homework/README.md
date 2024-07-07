## Unit and Integration tests

In this project we'll improve the reliability of our code with unit and integration tests. 

## Q1. Refactoring

Before we can start covering our code with tests, we need to 
refactor it. We'll start by getting rid of all the global variables. 

* Let's create a function `main` with two parameters: `year` and
`month`.
* Move all the code (except `read_data`) inside `main`
* Make `categorical` a parameter for `read_data` and pass it inside `main`

See: [batch.py](/06-best-practicies/homework/batch.py)

Now we need to create the "main" block from which we'll invoke
the main function. How does the `if` statement that we use for
this looks like? 

__Answer__: `if __name__ == '__main__':`

## Q2. Installing pytest

Now we need to install `pytest`:

```bash
pipenv install --dev pytest
```

Next, create a folder `tests` and create two files. One will be
the file with tests. We can name it `test_batch.py`. 

What should be the other file? 

__Answer__: `__init__.py`


## Q3. Writing first unit test

Now let's cover our code with unit tests.

We'll start with the pre-processing logic inside `read_data`.

It's difficult to test right now because first reads
the file and then performs some transformations. We need to split this 
code into two parts: reading (I/O) and transformation. 

So let's create a function `prepare_data` that takes in a dataframe 
(and some other parameters too) and applies some transformation to it.

Define the expected output and use the assert to make sure 
that the actual dataframe matches the expected one.

See: [test_batch.py](/06-best-practicies/homework/tests/test_batch.py)

How many rows should be there in the expected dataframe?

__Answer__: 2

## Q4. Mocking S3 with Localstack 

Now let's prepare for an integration test. In our script, we 
write data to S3. So we'll use Localstack to mimic S3.

First, let's run Localstack with Docker compose. Let's create a 
`docker-compose.yaml` file with just one service: localstack. Inside
localstack, we're only interested in running S3. 

Start the service and test it by creating a bucket where we'll
keep the output. Let's call it "nyc-duration".

See [docker-compose.yml](/06-best-practicies/homework/docker-compose.yml)

```bash
docker compose up -d
```

With AWS CLI, this is how we create a bucket:

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
```

Then we need to check that the bucket was successfully created. With AWS, this is how we typically do it:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
```

In both cases we should adjust commands for localstack. What option do we need to use for such purposes?

__Answer:__ --endpoint-url


## Make input and output paths configurable

Right now the input and output paths are hardcoded, but we want
to change it for the tests. 

One of the possible ways would be to specify `INPUT_FILE_PATTERN` and `OUTPUT_FILE_PATTERN` via the env 
variables. Let's do that:


```bash
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL=http://localhost:4566
```

And this is how we can read them:

```python
def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    # rest of the main function ... 
```


## Reading from Localstack S3 with Pandas

So far we've been reading parquet files from S3 with using
pandas `read_parquet`. But this way we read it from the
actual S3 service. Now we need to replace it with our localstack
one.

For that, we need to specify the endpoint url:

```python
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}

df = pd.read_parquet('s3://bucket/file.parquet', storage_options=options)
```

Let's modify our `read_data` function:

- check if `S3_ENDPOINT_URL` is set, and if it is, use it for reading
- otherwise use the usual way

See [batch.py](/06-best-practicies/homework/batch.py)


## Q5. Creating test data

Now let's create `integration_test.py`

We'll use the dataframe we created in Q3 (the dataframe for the unit test)
and save it to S3. You don't need to do anything else: just create a dataframe 
and save it.

We will pretend that this is data for January 2023.

Run the [integration_test.py](/06-best-practicies/homework/integration_test.py) script. After that, use AWS CLI to verify that the file was created. 

Use this snipped for saving the file:

```python
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)
```

```bash
python integration_test.py
```

Ouput:
```
2024-07-06 19:06:37       3620 in/2023-01.parquet

Total Objects: 1
   Total Size: 3620
```

What's the size of the file?

__Answer__: 3620


## Q6. Finish the integration test

We can read from our localstack s3, but we also need to write to it.

Create a function `save_data` which works similarly to `read_data`,
but we use it for saving a dataframe. 

Let's run the `batch.py` script for January 2023 (the fake data
we created in Q5). 

We can do that from our integration test in Python: we can use
`os.system` for doing that (there are other options too). 

Now it saves the result to localstack.

The only thing we need to do now is to read this data and 
verify the result is correct. 

See [integration_test.py](/06-best-practicies/homework/integration_test.py)

What's the sum of predicted durations for the test dataframe?

```
Total Objects: 1
   Total Size: 3019
     ride_id  predicted_duration
0  2023/01_0           23.197149
1  2023/01_1           13.080101
Sum of predicted durations 36.28
```
__Anwser:__ 36.28


## Running the test (ungraded)

The rest is ready, but we need to write a shell script for doing 
that.

See: [run.sh](/06-best-practicies/homework/run.sh)

