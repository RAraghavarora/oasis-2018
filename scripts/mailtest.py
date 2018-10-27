import sendgrid
from sendgrid.helpers.mail import *
from openpyxl import *
from registrations.models import *

API_KEY = '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'
body = '''
<p>Greetings from OASIS 18!</p>

<p>&nbsp;</p>

<p><strong>All BITSians as well as outstation participants are hereby requested to download the official OASIS &#39;18 app from the<u>&nbsp;link provided in the mail</u>&nbsp;(uninstall any previous versions of OASIS &#39;18 app&nbsp;<em>if any</em>). All further app updates shall be pushed through normal procedure i.e Google Play Store update or App Store update.</strong></p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>The features of the Official OASIS &#39;18 App are -</p>

<p>&nbsp;</p>

<p>1.<strong>&nbsp;OASIS Wallet</strong>&nbsp;: Tired of waiting in long lines to order food ? Lost your BITS-ID Card ? Don&#39;t want to carry cash around the campus ? Well we have a solution for all of this. Use the OASIS wallet. You can also add balance from your swd account (only for&nbsp;&nbsp;&nbsp;<u>BITSIANS</u>) . Amount remaining in your wallet shall be refunded back to your SWD account.You can also receive and transfer amounts from one wallet to another ( NOTE : Transferred amounts will be&nbsp;<u><strong>NON-REFUNDABLE</strong></u>&nbsp;). Directly place your order from the wallet - no need to wait in lines. ( PFA - the guide to use the wallet )</p>

<p>&nbsp;</p>

<p>2.&nbsp;<strong>QR Code based Prof Show signings/Entry&nbsp;</strong>: Every app user (BITSians and Registered Outstation Participants) can buy Prof Show tickets on their QR code (&nbsp;<em>OPEN OASIS APP --&gt; WALLET --&gt;STALLS --&gt; PROF SHOWS&nbsp;</em>). The verification and entry will also be done using the same QR Code. You can also view your signed Prof Shows using the &#39;SHOW TICKETS&#39; button on the home page of the app.</p>

<p>&nbsp;</p>

<p>3.&nbsp;<strong>Ongoing Events</strong>&nbsp;: With Ongoing events you can instantaneously find details about current ongoing events.</p>

<p>&nbsp;</p>

<p>4.<strong>&nbsp;Filters</strong>&nbsp;: You can sort and filter events according to categories, dates, venue, and also view favourite events.</p>

<p>&nbsp;</p>

<p>5.&nbsp;<strong>Notification</strong>&nbsp;: Stay notified and don&#39;t miss the buzz with the latest delivered to your phone via push notifications. Also we have a notice board, so that you can view important notifications later on as well.</p>

<p>&nbsp;</p>

<p>6.<strong>&nbsp;Maps</strong>&nbsp;: Don&#39;t get lost on the campus and find your way to your favourite event with the Maps feature.</p>

<p>&nbsp;</p>

<p>7.&nbsp;<strong>Reminder</strong>&nbsp;: Set reminders for the events that you don&#39;t want to miss.</p>

<p>&nbsp;</p>

<p>8.&nbsp;<strong>Emergency contact</strong>: The app has emergency contact numbers.</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p><u><strong>INSTRUCTIONS for QR Code</strong></u>:</p>

<p>&nbsp;</p>

<p>This time we bring you the QR Code based system for buying tickets for Prof Shows and also for wallet to wallet amount transfer during OASIS .</p>

<p>&nbsp;</p>

<p>For BITSians, to generate your profile card with your QR Code, go to Profile tab and login using your BITS mail.</p>

<p>&nbsp;</p>

<p><br />
<em><strong>You can download the Official OASIS App from this link :</strong></em></p>

<p><strong><em>&nbsp;</em></strong></p>

<p><strong><em>ANDROID&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</em></strong><em>&nbsp;</em>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; :&nbsp;&nbsp;<a href="https://bits-oasis.org/android" rel="noreferrer noreferrer" target="_blank">https://bits-oasis.org/android</a>&nbsp;&nbsp; &nbsp;</p>

<p>&nbsp;&nbsp;</p>

<p><em><strong>IOS &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</strong></em>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; :&nbsp;&nbsp;<a href="https://bits-oasis.org/ios/" rel="noreferrer noreferrer noreferrer" target="_blank">https://bits-oasis.org/ios</a></p>

<p>&nbsp;</p>

<p><strong><em>NON ANDROID / IOS&nbsp; DEVICES (Web Application)</em></strong>&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; :&nbsp;&nbsp;<a href="https://bits-oasis.org/2018/storewebapp/" rel="noreferrer noreferrer" target="_blank">https://bits-oasis.org/2018/storewebapp/&nbsp;</a></p>

<p>&nbsp;</p>

<p><em>NOTE: The web application does not require any download or installation and works on all platforms like<strong>&nbsp;android , iOS</strong>, windows etc as well.</em></p>

<p>&nbsp;</p>

<p>For&nbsp;<strong><u>Outstation participants</u></strong>, login using your allotted User ID and Password through the app or the site, which will generate your profile card with your QR code.</p>

<p>&nbsp;</p>

<p><strong><u>Link to download the wallet manual :</u>&nbsp;</strong><a href="https://bits-oasis.org/2018main/AppManual.pdf">https://bits-oasis.org/2018main/AppManual.pdf</a></p>

<p>&nbsp;</p>

<p><strong>For any queries call :&nbsp;</strong></p>

<p>&nbsp;</p>

<p><u>(DEPARTMENT OF VISUAL MEDIA)</u></p>

<p>&nbsp;</p>

<p>Nishant Mahajan&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;+91 9462180690</p>

<p>Tushar Goel&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; +91 9694345679</p>

<p>Manish Kumar Thakur&nbsp; &nbsp;+91 7989477976</p>

<p>Vaibhav Maheshwari&nbsp; &nbsp; &nbsp;+91 9529179518</p>

''' 




for i in Participant.objects.filter(firewallz_passed=True):
	sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
	send_to=i.email
	from_email = Email('no-reply@bits-oasis.org')
	to_email = Email(send_to)
	subject = "Official App for OASIS'18"
	content = Content('text/html', body)
	try:
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())
		print("Email "+i.email)
	except :
		print('Error in sending')


for i in Bitsian.objects.all():
	sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
	send_to=i.email
	from_email = Email('no-reply@bits-oasis.org')
	to_email = Email(send_to)
	subject = "Official App for OASIS'18"
	content = Content('text/html', body)
	try:
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())
		print("Email "+i.email)
	except :
		print 'Error in sending'
