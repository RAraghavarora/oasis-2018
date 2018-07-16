# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='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')
from_email = Email("raghavarora2012.ra@gmail.com")
email_list = ['f20171016@pilani.bits-pilani.ac.in', 'raghavarora2012.ra@gmail.com', 'raghavarora999@yahoo.in']

con = '''
Exception occured in the Website!

Error message is :
'''

def send_email():
    subject = "Exception occurred"
    content = Content("text/plain", con)    
    for i in email_list:
        to_email = Email(i)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
    print("MAIL = SENT")

#print(response.status_code)
#print(response.body)
#print(response.headers)