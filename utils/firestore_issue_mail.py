from django.utils import timezone
from oasis2018.sg import sg # For sendgrid
from sendgrid.helpers.mail import *

def send_mail(exception, model_name, action, data):
    email_list = [
        'f20171196@pilani.bits-pilani.ac.in',
        'f20171016@pilani.bits-pilani.ac.in',
        'f20170216@pilani.bits-pilani.ac.in',
        'f20170636@pilani.bits-pilani.ac.in',
        'f20171170@pilani.bits-pilani.ac.in',
        'f2016023@pilani.bits-pilani.ac.in',
        'f2016036@pilani.bits-pilani.ac.in',
        'f2016153@pilani.bits-pilani.ac.in',
        'f2015831@pilani.bits-pilani.ac.in',
    ]
    from_email = Email("f20171170@pilani.bits-pilani.ac.in")
    subject = "Unable To Communicate With Google Cloud Firestore"
    content = """
                    <p><strong>A serious exception has occured while trying to communicate with Firestore.</strong></p>

<p><em><u>Exception</u></em>: {}</p>

<p><em><u>Timestamp</u></em>: {}</p>

<p><em><u>Model</u></em>: {}</p>

<p><em><u>Data</u></em>: {}</p>

                """.format(exception, timezone.now(), "Balance", "Delete", data)
    for email in email_list:
        to_email = Email(email)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())
