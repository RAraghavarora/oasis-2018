#File to send an email to all the backend team in case of any exception in the website using SendGrid

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *
#####RAGHAV'S APIKEY #####
##### HAVE TO REPLACE THE API ####
API_KEY='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' 
sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
from_email = Email("webmaster@bits-oasis.org")

class add_guest(object):
	name = None
	verify_email_url = None
	body = '''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> 
            <center><img src="http://bits-oasis.org/2017/static/registrations/img/logo.png" height="150px" width="150px"></center>
            <pre style="font-family:Roboto,sans-serif">
Hello %s!

Thank you for registering!

Greetings from BITS Pilani!

It gives me immense pleasure in inviting your institute to the 48th edition of OASIS, the annual cultural fest of Birla Institute of Technology & Science, Pilani, India. This year, OASIS will be held from October 27th to October 31st.             
           
This is to inform you that your guest registration is complete.
You can now login in the app using the following credentials and get your exclusive qrcode:
username : '%s'
password : '%s'

Regards,
StuCCAn (Head)
Dept. of Publications & Correspondence, OASIS 2018
BITS Pilani
%s
pcr@bits-oasis.org
</pre>
'''
	x='register@bits-oasis.org'
	from_email = Email('register@bits-oasis.org')
	subject = "Registration for OASIS '18 THE FAR OUT FEST"	