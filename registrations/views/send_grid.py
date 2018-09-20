#File to send an email to all the backend team in case of any exception in the website using SendGrid

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='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')
from_email = Email("raghavarora2012.ra@gmail.com")


class register(object):
	name = None
	verify_email_url = None
	body = '''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<center><img src="http://bits-oasis.org/2017/static/registrations/img/logo.png" height="150px" width="150px"></center>
	<pre style="font-family:Roboto,sans-serif">
	Hello %s!

	Thank you for registering!

	Greetings from BITS Pilani!

	It gives me immense pleasure in inviting your institute to the 48th edition of OASIS, the annual cultural fest of Birla Institute of Technology & Science, Pilani, India. This year, OASIS will be held from October 27th to October 31st.

	Please apply as soon as possible to enable us to confirm your participation at the earliest.

	We would be really happy to see your college represented at our fest.

	We look forward to seeing you at OASIS 2018.

	<a href='%s'>Click Here</a> to verify your email.

	P.S: THIS EMAIL DOES NOT CONFIRM YOUR PRESENCE AT OASIS 2018. YOU WILL BE RECEIVING ANOTHER EMAIL FOR THE CONFIRMATION OF YOUR PARTICIPATION.

	Regards,
	StuCCAn (Head)
	Dept. of Publications & Correspondence, OASIS 2018
	BITS Pilani
	+91-80033 05723
	pcr@bits-oasis.org
	</pre>
	'''

	from_email = Email('register@bits-oasis.org')
	subject = "Registration for OASIS '18 THE FAR OUT FEST"

class cr_approved(object):
	name = None
	verify_email_url = None
	body = '''<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<center><img src="http://bits-oasis.org/2017/static/registrations/img/logo.png" height="150px" width="150px"></center>
	<pre style="font-family:Roboto,sans-serif">
	Hello %s!

	Thank you for registering!

	Greetings from BITS Pilani!

	It gives me immense pleasure in inviting your institute to the 48th edition of OASIS, the annual cultural fest of Birla Institute of Technology & Science, Pilani, India. This year, OASIS will be held from October 27th to October 31st.

	This is to inform you that your college representative has selected your participation.
	You can now login <a href="%s">here</a> using the following credentials:
	username : '%s'
	password : '%s'
	We would be really happy to see your college represented at our fest.

	Please make sure to upload your <b>Picture</b> as well as <b>verification documents(Eg Bonafide)</b> once you login to complete your registration.

	We look forward to seeing you at OASIS 2018.

	P.S: THIS EMAIL DOES NOT CONFIRM YOUR PRESENCE AT OASIS 2018. YOU WILL BE RECEIVING ANOTHER EMAIL FOR THE CONFIRMATION OF YOUR PARTICIPATION.

	Regards,
	StuCCAn (Head)
	Dept. of Publications & Correspondence, OASIS 2017
	BITS Pilani
	%s
	pcr@bits-oasis.org
	</pre>
	'''
	x='register@bits-oasis.org'
	from_email = Email('register@bits-oasis.org')
	subject = "Registration for OASIS '18"	