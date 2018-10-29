from shop.models.item import Tickets
from registrations.models import *
from events.models import *
import sendgrid
from sendgrid.helpers.mail import *
import uuid

API_KEY='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' #partho's api
sg = sendgrid.SendGridAPIClient(apikey=API_KEY) #


body='''
<pre>
<samp>Hello {0}!

This mail is regarding your signing for The EDM NITE Prof Show.

You have been signed {1} time(s).

Make sure to take a screenshot of your QR which will be necessary at the entrance.

You can get your qr code and profile details on the official OASIS 2018 android and iOS application by using your BITS Mail.

Below is an image of your qrcode which will be required at the entrance.
You can get your qr code here: {2}.

Controls,
BITS OASIS 2018</samp>
</pre>
'''


a = MainProfShow.objects.get(name__icontains = 'EDM')
c = 1
b = 1

for t in a.tickets.all():
    try:
        p = Bitsian.objects.get(user = t.user)
    except:
        continue
        # p = Bitsian.objects.get(user = t.user)
    if p.long_id[3] == '7' or p.long_id[3] == '8':
        pass
    else:
        continue
    send_to=['f20170216@pilani.bits-pilani.ac.in']
    from_email = Email('controls@bits-oasis.org')
    to_email = Email(send_to)
    u_uid = p.user.wallet.uuid
    subject = "QR Code for Hindi Prof Show OASIS 2018"
    url = 'https://bits-oasis.org/2018/storewebapp/qr/'+str(u_uid)
    body1 = body.format(p.name,str(t.count),url)
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


