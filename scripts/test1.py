import sendgrid
from sendgrid.helpers.mail import *


API_KEY='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' #my api


subject = 'College Representative for Oasis'
from_email = Email('register@bits-oasis.org')
to_email = Email('nayan1848@gmail.com')
content = Content('text/html', 'Hii')
sg = sendgrid.SendGridAPIClient(apikey=API_KEY) #

mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(type(response.status_code))