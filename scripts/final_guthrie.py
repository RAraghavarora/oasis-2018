from shop.models.item import Tickets
from registrations.models import *
from events.models import *
import sendgrid
from sendgrid.helpers.mail import *
import uuid


body='''
<pre>
Hello {0}!
This mail is regarding your signing for The English ProfShow.
You have been signed {1} times.
Also, your QR code number is {2}.

Make sure to take a screenshot of your QR which will be necessary at the entrance.

You can get your qr code and profile details on the official OASIS 2018 android and iOS application by using your BITS Mail.

Below is an image of your qrcode which will be required at the entrance.
You can get your qr code here: {3}.

Controls,
BITS OASIS 2018
</pre>
<p>&nbsp;</p>

<div>
<p style="margin-left:0px; margin-right:0px"><span style="color:#313131"><strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<u>PROF-SHOW ENTRY PLAN</u></strong></span></p>

<p style="margin-left:0px; margin-right:0px">&nbsp;</p>
This Oasis, entry to the Auditorium for&nbsp;<strong>English Prof Show</strong>-&nbsp;<strong>Guthrie Govan&nbsp;</strong>with QR Code is as follows:

<div>
<ol>
	<li><strong>All Girls</strong>&nbsp;irrespective of their QR&nbsp;number should enter only from&nbsp;<strong>FD-3 building</strong>&nbsp;<strong>lower</strong>&nbsp;corridor connection to Auditorium.</li>
	<li>Boys with stub numbers&nbsp;<strong>1-400</strong>&nbsp;shall enter from&nbsp;<strong>FD-2 building lower&nbsp;</strong>corridor connection to Auditorium.</li>
	<li>Boys with stub numbers&nbsp;<strong>401-800</strong>&nbsp;shall enter from&nbsp;<strong>FD-2 building upper&nbsp;</strong>corridor connection to Auditorium.</li>
	<li>Boys with stub numbers<strong>&nbsp;801 and above</strong>&nbsp;shall enter from&nbsp;<strong>FD-3 building upper</strong>&nbsp;corridor connection to Auditorium.</li>
	<li>All On-Spot Entries are through the main Audi gate.</li>
</ol>

<div><strong>The entry for the Prof show will only be through QR code. You can find your QR code in the Profile section of Oasis App.</strong></div>
It is mandatory to carry&nbsp;<strong>BITSIAN ID</strong>&nbsp;cards along with your QR code when you enter the Auditorium.</div>

<div>Make sure to have a screenshot of your QR code and enough battery on your phone just in case.</div>

<div>&nbsp;</div>

<div><strong>Bags</strong>&nbsp;and&nbsp;<strong>Eatables</strong>&nbsp;are not allowed into the Auditorium during the prof show.</div>

<div>Bringing any&nbsp;<strong>intoxicating substance</strong>&nbsp;is strictly&nbsp;prohibited and strict action will be taken against people found guilty by the institute.</div>

<div>&nbsp;</div>

<div>
<p><em><strong>You can download the Official OASIS App from this link :</strong></em></p>

<p><strong><em>ANDROID&nbsp;</em></strong>:&nbsp;&nbsp;<a href="https://u7689750.ct.sendgrid.net/wf/click?upn=6vlC1qlrAJUlbya7dkP3rx-2B76sv0RizPEz31sqZ6ii0wyXmZQgcXmorNhgIJt6wK_FRV3-2Bch4TgQodHJ4dKzIlYQjskXUJkZAZFlQX5UMrrIq7miUYUF98OS-2FsYHjrRpM5Fc67SBGQtHP4MmtKjxMU-2FvzXidpT-2FCKwE2RQXkuca-2FY-2BeYUMnk4T0Pj3e8omcZtOhCsHyHqE38-2FNYHm9QDjrmIFeLIDcPc8h-2BNg2ULN7U86RPaRjme-2FmFCYt-2FMrvNzv1z1gGt-2BxgV6zpHBxZQGSvIrDi-2FPJQxVFOOhwLepuFmU-3D" rel="noreferrer noreferrer" style="color:#1155cc" target="_blank">https://bits-oasis.org/android</a>&nbsp; &nbsp;&nbsp;</p>

<p><em><strong>IOS&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;</strong></em>:&nbsp;&nbsp;<a href="https://u7689750.ct.sendgrid.net/wf/click?upn=6vlC1qlrAJUlbya7dkP3r1AFglfp2-2Be-2B3zPsXH-2BCn6MTwUWfbRFxgy8XyzTqNxev_FRV3-2Bch4TgQodHJ4dKzIlYQjskXUJkZAZFlQX5UMrrIq7miUYUF98OS-2FsYHjrRpM5Fc67SBGQtHP4MmtKjxMU64MY0imZL-2Fg2oUG59rfNw7WcO8SZuul44RycCrzBrfIyY22yofQq8DVp8G6YsFmrSS-2F1swGVbtr3cSMLOpKuvPTG1Lvhus6mc9R3FaJiWxtfb4Uho66YR6UobUw5VF8X6NQwIbR7YKjB0hOgP1i9m0-3D" rel="noreferrer noreferrer noreferrer" style="color:#1155cc" target="_blank">https://bits-oasis.org/ios</a></p>

<p>&nbsp;<strong><em>NON ANDROID / IOS&nbsp; DEVICES (Web Application)</em></strong>:&nbsp;&nbsp;<a href="https://u7689750.ct.sendgrid.net/wf/click?upn=6vlC1qlrAJUlbya7dkP3r9CvF-2F44nd6gsINM6vYl2B7vKi4YMPnk-2F5VwwJUJaUHk_FRV3-2Bch4TgQodHJ4dKzIlYQjskXUJkZAZFlQX5UMrrIq7miUYUF98OS-2FsYHjrRpM5Fc67SBGQtHP4MmtKjxMU2gAbWqWGxgUHJlcNmIxogt3ax1kalhicyqI34E5ZXNk5g353YAHry4z9xfFh2x9xtSp45LLtAFPCTgFDPiDpkzRuHQB-2BSeYXsaSarHSUokFK9fAclBpLUEEe09DVTJYi1vw9j7Bls6y9eqE2iEkvgk-3D" rel="noreferrer noreferrer" style="color:#1155cc" target="_blank">https://bits-oasis.org/2018/storewebapp/&nbsp;</a></p>
</div>

<div>&nbsp;</div>

<div>&nbsp;</div>

<div>Cheers!</div>

<div>Audiforce</div>

<div>&nbsp;</div>

<div>For any queries regarding entry contact:</div>

<div>Sailesh Reddy</div>

<div>Coordinator</div>

<div>Audiforce</div>

<div>9829299429</div>

<div>&nbsp;</div>

<div>For any other queries regarding the prof show contact:</div>

<div>Pankaj Tawale</div>

<div>ARBITS</div>

<div>7689078289</div>
</div>

<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div><strong>Sailesh Reddy</strong>

<div>
<div><span style="color:#888888"><span style="color:#888888"><span style="background-color:#ffffff">Coordinator,</span></span></span></div>

<div><span style="color:#888888"><span style="color:#888888"><span style="background-color:#ffffff">Audiforce</span></span></span></div>

<div><span style="color:#888888"><span style="color:#888888"><span style="background-color:#ffffff">Oasis&#39;18, BITS Pilani</span></span></span></div>

<div>&nbsp;</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
'''


a = MainProfShow.objects.get(name__icontains = 'Guthrie')
c = 1
b = 1
for t in a.tickets.all():
    try:
        p = Participant.objects.get(user = t.user)
    except:
        p = Bitsian.objects.get(user = t.user)
    send_to=p.email
    from_email = Email('controls@bits-oasis.org')
    to_email = Email(send_to)
    u_uid = p.user.wallet.uuid
    subject = "QR Code for English Prof Show OASIS 2018"
    url = 'https://bits-oasis.org/storewebapp/qr/'+str(u_uid)
    body = body.format(p.name,str(t.count),str(c),url)
    content = Content('text/html', body)
    c+=t.count
    b+=1
    print(c)
    try:
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code%100!=2:
            print("*******")
            raise Exception
        print("Email sent to "+str(send_to))
    except Exception as e:
        print('Mail not sent to '+str(send_to))


