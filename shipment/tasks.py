from celery import shared_task

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import requests
from .models import *

# Celery Commands

'''
# celery worker --loglevel=info
# celery -A mysite worker -l info
# celery -A mysite beat -l info
# pkill -9 celery
# celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
'''


#shipment request configuration
def request_conf(token):
    myUrl = 'https://api.bol.com/retailer/shipments/?fulfilment-method=FBB'
    head = {'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/vnd.retailer.v3+json',
            'Accept':'application/vnd.retailer.v3+json'}
    r = requests.get(myUrl, headers=head)
    return r


@periodic_task(run_every=timedelta(seconds=299))
def login():
    '''
    Runs in every 299 seconds for  refreshing token
    '''

    client = BackendApplicationClient(client_id="808b78c3-e285-4a02-8b78-22e02c260c41")
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://login.bol.com/token', client_id="808b78c3-e285-4a02-8b78-22e02c260c41",
        client_secret="FV8z1j-v2k5abnLQudTfFhzed1gCRfQGWBucbtFgkDK-Qy8xwwdgrG1MZDBPrL0SxIYdeUhWrV7KNtH06bRTvg")   
    token = token['access_token']
    token = AuthToken.objects.create(token=token)
    return token


#Get shipment list within 7 request in 60 secs
@periodic_task(run_every=timedelta(seconds=8.57))
def sync_shipment():
    token = AuthToken.objects.last()
    token = token.token  

    r = request_conf(token)
    """
    if somehow celery stop working
     to get new auth token
    """    
    if r.status_code == 401:
        print('Token is expire.')
        token = login()
        r = request_conf(token)


    for s in r.json()['shipments']:
        if not Shipment.objects.filter(shipment_id=s['shipmentId']):
            print('No Shipment found')
            ship = Shipment.objects.create(shipment_id=s['shipmentId'], 
                                    shipment_ref=s['shipmentReference'], 
                                    shpiment_date=s['shipmentDate'])

            Transport.objects.create(shipment=ship,
                                                transport_id=s['transport']['transportId'])  

            for i in s['shipmentItems']:
                ShipmentItem.objects.create(shipment=ship, 
                                                order_item_id=i['orderItemId'], 
                                                order_id=i['orderId'])
                                

    return 'Successfully Sync'


