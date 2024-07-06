import os
import model

RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init(
    run_id=RUN_ID,
    test_run=TEST_RUN
)

def lambda_handler(event):
    return model_service.lambda_handler(event)