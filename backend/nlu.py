import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

IAM_Authenticator = os.getenv('IBM_IAM_AUTHENTICATOR')
IBM_Service_Instance = os.getenv('IBM_SERVICE_URL')

# Authentication via IAM
def nlu(comment):
    authenticator = IAMAuthenticator(IAM_Authenticator)
    service = NaturalLanguageUnderstandingV1(
        version='2018-03-16',
        authenticator=authenticator)
    service.set_service_url(IBM_Service_Instance)

    response = service.analyze(
        text=comment,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()
    # print(json.dumps(response,indent=2))
    return response

