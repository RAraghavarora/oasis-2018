import sendgrid
from sendgrid.helpers.mail import *
from registrations.models import *
import uuid

# API_KEY = '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'
API_KEY= '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'

body = '''
<pre>
Hello {0}!
This mail is regarding your signing for The English ProfShow.
You have been signed {1} times.
Also, your QR code number is {2}.
Below is an image of your qrcode which will be required at the entrance.
You can get your qr code here: {3}.

Make sure to take a screenshot of your QR which will be necessary at the entrance.

You can get your qr code and profile details on the official OASIS 2018 android and iOS application by using your BITS Mail.


Controls,
BITS OASIS 2018
</pre>
'''


list1=['raghavarora2012.ra@gmail.com','f20171016@pilani.bits-pilani.ac.in','nayan1848@gmail.com']
a=1
sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

for i in list1:
    send_to=i
    from_email = Email('dvm@bits-oasis.org')
    to_email = Email(send_to)
    subject = "QR Code for English Prof Show OASIS 2018"
    u_uid = uuid.uuid4()
    url = '127.0.0.1:8000/storewebapp/qr/'+str(u_uid)
    body = body.format('DVM','56',str(a),url)
    content = Content('text/html', body)

    a+=1
    try:
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code%100!=2:
            print("***")
            raise Exception
        print("Email sent to "+str(send_to))
    except Exception as e:
        print(e)
        print('Mail not sent to '+str(send_to))


# for i in Participant.objects.filter(firewallz_passed=True):
#     sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
#     send_to=i.email
#     uuid = i.user.wallet.uuid
#     url = 'bits-oasis.org/storewebapp/qr/'+uuid
#     from_email = Email('no-reply@bits-oasis.org')
#     to_email = Email(send_to)
#     subject = "Official App for OASIS'18"
#     content = Content('text/html', body)
#     try:
#         mail = Mail(from_email, subject, to_email, content)
#         response = sg.client.mail.send.post(request_body=mail.get())

#         print("Email "+i.email +" "+ str(cnt1))
#         cnt1+=1
#     except :
#         print('Error in sending')

#         print("Email "+i.email +" "+ str(i))




# for i in Bitsian.objects.all():
#     sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
#     send_to=i.email
#     from_email = Email('no-reply@bits-oasis.org')
#     to_email = Email(send_to)
#     subject = "Official App for OASIS'18"
#     content = Content('text/html', body)
#     try:
#         mail = Mail(from_email, subject, to_email, content)
#         response = sg.client.mail.send.post(request_body=mail.get())
#         print("Email "+i.email)
#     except :
#         print ('Error in sending')

