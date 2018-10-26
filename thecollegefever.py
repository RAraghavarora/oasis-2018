#!/usr/bin/python

# update_database.py

'''
    Update "Payment Status" to True for participants who have successfully paid through CollegeFever.
    Scraping of excel sheet in CollegeFever Account Dashboard. 
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oasis2018.settings')

import django
django.setup()

import requests

import json

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
    

import datetime

from registrations.models import Participant, College
from events.models import *



try:
    login_url = 'https://www.thecollegefever.com/v1/auth/basiclogin'
    headers = {'Content-Type': 'application/json'}
    login_data = {"email":"webmaster@bits-oasis.org","password":"Ashujain@1997"} 

    login_response = requests.post(url=login_url, headers=headers, data=json.dumps(login_data))
    # status_code = login_response.status_code
    json_ob = json.loads(login_response.text)
    session = json_ob['sessionId']
    cookies = {'auth':session}

    url = 'https://www.thecollegefever.com/v1/analytics/eventanalytics?id=4148'
    response = requests.get(url=url, headers=headers, cookies=cookies)
    json_ob2 = json.loads(response.text)
    html_data = json_ob2['reportHtml']

    raw_body_data = BeautifulSoup(html_data, features='html.parser')("tbody")
    body_data = str(raw_body_data).strip('[')[:-1]
    table_data = [[cell.text for cell in row("td")]
                            for row in BeautifulSoup(body_data, features='html.parser')("tr")]
    '''
    #########   Sample table_data <class: 'list'> List Type Object  ########
    [
        ['SHIVANGI ROHILLA', 'shivangirohilla2010@gmail.com', '8168369099', 'Institute Of Home Economics (Delhi University) , Hauz Khas',
        'Registration', 'KMNGYXC', '1000.00', 'null', 'BENGALURU', 'null', 'Thu Oct 18 12:41:18 IST 2018'], 

        ['Jyoti', 'jyotibs97@gmail.com', '7042583672', 'Institute Of Home Economics (Delhi University) , Hauz Khas',
        'Registration', '3D49PKY', '1000.00', 'null', 'BENGALURU', 'null', 'Thu Oct 18 13:28:07 IST 2018']
    ]
    '''

    index = 0
    ids= []
    count=0
    for index, entry in enumerate(table_data):
        email = entry[1]
        count+=1
        try:
            participant = Participant.objects.get(email=email)
            if participant.id in ids:
                print('Duplicate User %s'%email)
            ids.append(participant.id)
        except:
            print('Participant with %s doesnt exist')%email

    print(ids)
    print(count)

except:
    print('Couldn\'t reach the college fever website. ')

        


                
