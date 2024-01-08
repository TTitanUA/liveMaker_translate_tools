import json
import requests
import uuid
from config import AZURE_API_KEY, AZURE_API_ENDPOINT, AZURE_API_REGION

path = '/translate'


def azure_translate(texts, from_lang='ja', to_lang='en'):
    constructed_url = AZURE_API_ENDPOINT + path

    params = {
        'api-version': '3.0',
        'to': to_lang
    }

    if from_lang != 'auto':
        params['from'] = from_lang

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_API_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_API_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    body = []

    for text in texts:
        body.append({'text': text})

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    print(response)

    result = []
    for translation in response:
        result.append(translation['translations'][0]['text'])

    return result
