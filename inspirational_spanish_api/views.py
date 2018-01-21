import json
import os

import requests
from django.http import HttpResponse
from google.cloud import translate
from django.conf import settings
from google.oauth2 import service_account


def index(request):
    payload = {'method': 'getQuote', 'format': 'json', 'lang': 'en'}
    r = requests.get('http://api.forismatic.com/api/1.0/', params=payload)
    data = json.loads(r.text)

    # Imports the Google Cloud client library
    if settings.DEBUG:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{0}/keys/Inspirational-Quotes-Spanish-457f10e4eb96.json'.format(
            os.path.dirname(os.path.abspath(__file__)))
        translate_client = translate.Client()
    else:
        info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
        creds = service_account.Credentials.from_service_account_info(info)
        # Instantiates a client
        translate_client = translate.Client(credentials=creds)

    # The text to translate
    text = u'%s' % data['quoteText']
    # The target language
    target = 'es'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    data['quoteText'] = translation['translatedText']

    return HttpResponse(json.dumps(data), content_type='application/json')
