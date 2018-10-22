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

def update_database():

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
        # print(response.status_code)
        # print(response.text)
        json_ob2 = json.loads(response.text)
        # print(json_ob2)
        html_data = json_ob2['reportHtml']
        # print(html_data)
        # print(type(html_data))

        raw_body_data = BeautifulSoup(html_data, features='html.parser')("tbody")
        # print(type(raw_body_data))
        # print(raw_body_data)
        body_data = str(raw_body_data).strip('[')[:-1]
        # print(type(body_data))
        # print(body_data)
        table_data = [[cell.text for cell in row("td")]
                                for row in BeautifulSoup(body_data, features='html.parser')("tr")]
        # print(table_data)
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
        for index, entry in enumerate(table_data):
            email = entry[1]
            amount = int(float(entry[6]))
            # print(type(amount))
            name= entry[0]
            phone = int(entry[2])
            college = entry[3]
            # clg, created = College.objects.get_or_create(name=college)
            # participant, created = Participant.objects.get_or_create(name=name, email=email, phone=phone, college=clg)
            participant = Participant.objects.get(email=email)
            
            if amount == 1000:
                participant.paid = True
                participant.controlz_paid = True
            elif amount == 300:
                participant.paid = True
            elif amount == 700:
                participant.controlz_paid = True

            participant.save()
            ''' Yipppeeee!! Now I am registered. '''

        return 'All entries upto {} updated successfully.'.format(len(table_data))


    except Exception as error:
        print(error)
        return "There was an error in updating database. {} entries from the top updated.".format(index)

if __name__ == '__main__':
	print(str(datetime.datetime.now())+ " : Starting Database Updation Script...")
	message = update_database()
	print(str(datetime.datetime.now()) + ' : ' + message)
