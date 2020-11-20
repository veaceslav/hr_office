import json
import logging
from odoo_utils import odoo_api_login, update_applicant_stage, write_note_to_the_applicant, refuse_candidate
from classmarker_utils import parse_classmarker_result
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ODOO_URL = "https://davinciderivatives.odoo.com"
ODOO_DB = "davinciderivatives"
ODOO_USER = "ops@davinciderivatives.com"
ODOO_PASSWORD = "926b1f4cfc961de49a89c7f1c3705ab8b1056c00"

NEXT_INTERVIEW_STAGE = 4

# we configured this in Odoo as "Test Results too low"
REFUSAL_REASON_ID = 4
    
def lambda_handler(event, context):
    
    logger.info(event)
    

    access = odoo_api_login(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD)
    
    #write_note_to_the_applicant(access, 1, "hello", "Random message from Amazon lambda")
    
    user_id, result, incorrect, error = parse_classmarker_result(event)

    if(result - incorrect < 20):
        write_note_to_the_applicant(access, user_id, "Test failed", f"Candidate did not pass the test: Result: {result} "
                                                              f"Incorrect: {incorrect} Total Score: {result - incorrect} ")
        refuse_candidate(access, user_id, REFUSAL_REASON_ID)
    else:
        write_note_to_the_applicant(access, user_id, "Test failed", f"Candidate passed the test: Result: {result} "
                                                              f"Incorrect: {incorrect} Total Score: {result - incorrect} ")
        update_applicant_stage(access, user_id, NEXT_INTERVIEW_STAGE)

    return {
        'statusCode': 200,
        'body': json.dumps('')
    }
