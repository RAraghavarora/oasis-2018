from shop.models.item import Tickets
from registrations.models import *
from events.models import *
import sendgrid
from sendgrid.helpers.mail import *
import uuid

API_KEY='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' #raghav's api
sg = sendgrid.SendGridAPIClient(apikey=API_KEY) #


body='''
<pre>
<samp>Hello {0}!

This mail is regarding your signing for The EDM NITE Prof Show.

You have been signed {1} time(s).
Also, your QR code number is {2}.

Make sure to take a screenshot of your QR which will be necessary at the entrance.

You can get your qr code and profile details on the official OASIS 2018 android and iOS application by using your BITS Mail.

Below is an image of your qrcode which will be required at the entrance.
You can get your qr code here: {3}.

Controls,
BITS OASIS 2018</samp>
</pre>
'''


a = MainProfShow.objects.get(name__icontains = 'EDM')
c = 1
b = 1

for t in a.tickets.all():
    try:
        p = Participant.objects.get(user = t.user)
    except:
        p = Bitsian.objects.get(user = t.user)
    send_to=['f20170216@pilani.bits-pilani.ac.in']
    from_email = Email('controls@bits-oasis.org')
    to_email = Email(send_to)
    u_uid = p.user.wallet.uuid
    subject = "QR Code for EDM NITE"
    url = 'https://bits-oasis.org/2018/storewebapp/qr/'+str(u_uid)
    body1 = body.format(p.name,str(t.count),str(c),url)
    t.qr_no = c
    t.save()
    content = Content('text/html', body1)
    c+=t.count
    b+=1
    print(b,'\t',c)
    try:
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code%100!=2:
            print("*******")
            raise Exception
        print("Email sent to "+str(send_to))
    except Exception as e:
        print('Mail not sent to '+str(send_to))


