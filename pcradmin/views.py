from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from registrations.models import *
from events.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from functools import reduce
from registrations.urls import *
from registrations.views import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from oasis2018.settings import BASE_DIR
import sendgrid
import os
import re
from sendgrid.helpers.mail import *
import xlsxwriter
from time import gmtime, strftime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from oasis2018.keyconfig import *
import string
from django.contrib import messages

from random import choice

@staff_member_required
def index(request):
    return  redirect('pcradmin:college')

@staff_member_required
def college(request):
    rows = [{'data':[college.name,college.participant_set.filter(pcr_approved=True).count(),college.participant_set.filter(email_verified=True).count()],'link':[{'title':'Manage CR', 'url':reverse('pcradmin:select_college_rep', kwargs={'id':college.id})},{'title':'Approve Participations', 'url':reverse('pcradmin:approve_participations', kwargs={'id':college.id})}] } for college in College.objects.all()]
    tables=[{'title':'List of colleges',
    'rows':rows,'headings':['College','Confirmed','Total Particpants','Manage College Rep','Approve participations']}]
    return render(request, 'pcradmin/tables.html',{'tables':tables})


@staff_member_required
def select_college_rep(request,id):
    college=get_object_or_404(College,id=id)
    if request.method=='POST':
        data=request.POST
        try:
            part_id=data['data']
        except:
            messages.warning(request,'Select a participant')
        return redirect(request.META.get('HTTP_REFERER'))

## review
        if data['submit']=='delete':
            part=Participant.objects.get(id=part_id)
            user=part.user
            user.delete()
            part.user=None
            part.is_cr=False
            part.cr_approved=False
            part.save()
        elif data['submit']=='select':
            try:
                Participant.objects.get(college=college,is_cr=True)
                messages.warning(request,'Already selected as college rep')
                return redirect(request.META.get('HTTP_REFERER'))
            except:
                pass
            part=Participant.objects.get(id=part_id)
            part.is_cr=True
            part.cr_approved=True

            #Barcode generation here left for now. To be discussed if only QR or not
            part.save()
            user=part.user
            if not user==None:
                messages.warning(request,'College Representative already selected.')
                return redirect(request.META.get('HTTP_REFERER'))
            if user==None:
                username=part.name.split()[0]+str(part_id)
                length=8
                chars = string.letters + string.digits
                password = ''.join(choice(chars) for _ in xrange(length))
                user=User.objects.create(username=username,password='')
                user.set_password(password)
                user.save()
                part.user=user
                part.save()
            body = """<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> 
			<center><img src="http://bits-oasis.org/2017/static/registrations/img/logo.png" height="150px" width="150px"></center>
			<pre style="font-family:rowsboto,sans-serif">
Hello %s!

Thank you for registering!

Greetings from BITS Pilani!

It gives me immense pleasure in inviting your institute to the 48th edition of OASIS, the annual cultural fest of Birla Institute of Technology & Science, Pilani, India. This year, OASIS will be held from October 27th to October 31st.             
           
This is to inform you that you have been selected as the College Representative for your college.
You can now login <a href="%s">here</a> using the following credentials:
username : '%s'
password : '%s'
We would be really happy to see your college represented at our fest.
It is your responsibility to confirm the participants for different events.

Please make sure to upload your <b>Picture</b> as well as <b>verification documents(Preferably Bonafide Certificate for as many participants as possible)</b> once you login to complete your registration.

We look forward to seeing you at OASIS 2018.

P.S: THIS EMAIL DOES NOT CONFIRM YOUR PRESENCE AT OASIS 2018. YOU WILL BE RECEIVING ANOTHER EMAIL FOR THE CONFIRMATION OF YOUR PARTICIPATION. 

Regards,
StuCCAn (Head)
Dept. of Publications & Correspondence, OASIS 2018
BITS Pilani
%s
pcr@bits-oasis.org
</pre>
			""" %(part.name,str(request.build_absolute_uri(reverse('registrations:home'))),username, password,1234567890 ) #get_pcr_number()
            subject = 'College Representative for Oasis'
            from_email = Email('register@bits-oasis.org')
            to_email = Email(part.email)
            content = Content('text/html', body)
            #sg = sendgrid.SendGridAPIClient(apikey=API_KEY) Email validation not done
            try:
                mail = Mail(from_email, subject, to_email, content)
               # response = sg.client.mail.send.post(request_body=mail.get())
                messages.warning(request,'Email sent to ' + part.name)
            except :
                part.user = None
                part.is_cr = False
                user.delete()
                part.save()
                messages.warning(request,'Email not sent. Please select College Representative again.')
            return redirect(request.META.get('HTTP_REFERER'))
        participants=college.participant_set.filter(email_verified=True)
        try:
            cr = Participant.objects.get(college=college, is_cr=True)
            participants = participants.exclude(id=cr.id)
        except:
            cr=[]
        parts = [{'data':[part.name, part.phone, part.email, part.gender, part.pcr_approved, part.head_of_society, part.year_of_study, event_list(part),is_profile_complete(part), how_much_paid(part)], "id":part.id,} for part in participants]
        return render(request, 'pcradmin/college_rep.html',{'college':college, 'parts':parts, 'cr':cr})

###HELPER FUNCTIONS WRT TO THE ABOVE VIEW###
def event_list(part):
    events=''
    for participation in MainParticipation.objects.filter(participant=part):
        events+=participation.event.name +','
    events=events[:-2]
    return events
def is_profile_complete(part):
    try:
        profile_url=part.profile_pic.url
        docs_url=part.verify_docs.url
        return True
    except:
        return False
def how_much_paid(part):
    if part.controlz_paid or part.curr_controlz_paid:
        return 950
    if part.paid or part.curr_paid:
        return 300
    return 0

@staff_member_required
def approve_participations(request,id):
    college=get_object_or_404(College,id=id)
    try:
        cr=Participant.objects.get(college=college,is_cr=True)
    except:
        messages.warning(request,'College Rep not yet selected. Please select a college rep first for '+college.name)
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method=='POST':
        data=request.POST
        print(data)
        try:
            part_list=data.getlist('data')
        except:
            return redirect(request.META.get('HTTP_REFERER'))
        if data['submit']=='approve':
            for participation in MainParticipation.objects.filter(id__in=part_list):
                participation.pcr_approved=True
                participant=particpation.participant
                participant.pcr_approved=True
                participant.save()
                participation.save()
            message="Profile verified"
        elif data['submit']=='disapprove':
            for participation in MainParticipation.objects.filter(id__in=part_list):
                participation.pcr_approved=False
                participation.save()
                participant=participation.participant
                list_particpation=[]
                for part in MainParticipation.objects.filter(participant=participant):
                    if(not part.pcr_approved):
                        list_particpation.append(part)
                if all(list_particpation):   #Still not sure about it's working
                    participant.pcr_approved=False
                    participant.save()
            message="Events successfully unconfirmed"
        messages.success(request,message)
        approved=MainParticipation.objects.filter(pcr_approved=True,participant__college=college,cr_approved=True)
        disapproved=MainParticipation.objects.filter(pcr_approved=False,participant__college=college,cr_approved=True)
        return render(request, 'pcradmin/approve_participations.html', {'approved':approved, 'disapproved':disapproved, 'cr':cr})

@staff_member_required
def add_college(request):
    if request.method=='POST':
        data=request.POST
        if data['submit']=='add':
            try:
                name=request.POST['name']
                if name=='':
                    raise Exception
            except:
                messages.warning(request,'Please don\'t leave the name field empty. ')
                return redirect(request.META.get('HTTP_REFERER'))
            College.objects.create(name=name)
            messages.warning(request, 'College succesfully added')
            return redirect('pcradmin:add_college')
        elif data['submit']=='delete':
            college=College.objects.get(id=data['data'])
            college.delete()
            messages.warning(request, 'College succesfully deleted')
            return redirect('pcradmin:add_college')
        rows = [{'data':[college.name, college.participant_set.all().count(),  college.participant_set.filter(pcr_approved=True).count()], 'id':college.id, 'link':[{'title':'Select College Representative', 'url':reverse('pcradmin:select_college_rep', kwargs={'id':college.id})}]} for college in College.objects.all()]
        headings = ['Name', 'Registered Participants' , 'PCr approved Participants', 'Select/Modify CR']
        title="College List"
        table = {
        'rows':rows,
        'headings':headings,
        'title':title,
    }
    return render(request, 'pcradmin/add_college.html', {'table':table})

@staff_member_required
def edit_participant(request,part_id):
    participant=get_object_or_404(Participant,id=part_id)
    if request.method=='POST':
        data=request.POST
        try:
            name=data['name']
            phone=data['phone']
            email=data['email']
            gender=data['gender']
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) or not gender in ['M','F'] or len(phone) is not int(10):
                raise Exception
        except:
            messages.warning(request, 'Fill all the details properly.')
            return request.META.get('HTTP_REFERER')
        participant.name=name
        participant.phone=phone
        participant.email=email
        participant.gender=gender
        participant.save()
        return redirect(reverse('pcradmin:select_college_rep', kwargs={'id':participant.college.id}))
    return render(request,'pcradmin/edit_part.html',{'particpant':participant})




################      STATS       ####################            
@staff_member_required
def stats(request, order=None):
    if order==None:
        order='collegewise'
    if order=='collegewise':
        rows = []
        for college in College.objects.all():
            participants = college.participant_set.all()
            try:
                cr_participant = participants.filter(is_cr=True)[0]
                cr = 'True (' + cr_participant.name + ')'
            except:
                cr = False
            
            male_participants = participants.filter(gender='M')
            female_participants = participants.filter(gender='F')
            display_data = {
                'data': [
                    college.name, cr, participants_count(male_participants),
                    participants_count(female_participants), participants_count(participants),
                    profile_stats(participants)
                ],
                'link' : []
            }    
            rows.append(display_data)
        participants = Participant.objects.all()
        male_participants = participants.filter(gender='M')
        female_participants = participants.filter(gender='F')
        display_data = {
            'data': [
                'Total', ' ', participants_count(male_participants),
                participants_count(female_participants), participants_count(participants),
                ' - - '
            ],
            'link' : []
        }
        rows.append(display_data)
        headings = [
            'College', 'CR Selected', 'Male', 'Female', 'Stats', 'Profile Status' 
        ]
        title = 'CollegeWise Participants Stats'
        context = {
            'tables': [
                {'rows': rows, 'headings': headings, 'title':title}
            ]
        }
        return render(request, 'pcradmin/tables.html', context)
    
    if order == 'eventwise':
        rows = []
        for event in MainEvent.objects.all().iterator():
            participants = event.participant_set.all()
            if participants.count()>0:
                male_participants = participants.filter(gender = 'M')
                female_participants = participants.filter(gender = 'F')
                display_data = {
                    'data': [
                        event.name, event.category, participants_count(male_participants),
                        participants_count(female_participants), participants_count(participants) 
                    ],
                    'link' : [
                        { 'title': 'View', 'url': reverse('pcradmin:stats_event', kwargs={'e_id': event.id})}
                    ]
                }
                rows.append(display_data)
        headings = ['Event', 'Category', 'Male', 'Female', 'Total', 'View']
        title = 'EventWise Participants Stats'
        context = {
            'tables': [
                {'rows': rows, 'headings': headings, 'title': title},   
            ]
        }
        return render(request, 'pcradmin/tables.html', context) 

    if order == 'paidwise':
        for participant in Participant.objects.filter(Q(pcr_approved=True), Q(paid=True)|Q(curr_paid=True)):
            display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, get_payment_status(participant),
                    get_event_status(participant)
                ],
                'link' : []
            }
            headings = ['Name', 'College', 'Gender', 'Phone', 'Email', 'Payment Made', 'Events']
            title = "Participant's Payment Status"
            context = {
                'tables': [
                    {'rows': rows, 'headings': headings, 'title': title},   
                ]
            }
            return render(request, 'pcradmin/tables.html', context)

@staff_member_required
def stats_event(request, e_id):
    event = get_object_or_404(MainEvent, id = e_id)
    rows = []
    for college in College.objects.all():
        participants1 = college.participant_set.filter(email_verified=True)
        participants = Participant.objects.filter(id__in = [
            participant.id for participant in participants1 if MainParticipation.objects.filter(participant = participant, event = event)
        ]) #participants of that college in this event whose email has been verified.
        if not participants:
            continue
        try:
            cr_participant = participants.filter(is_cr = True)[0]
            cr = 'True (' + cr_participant.name + ')'
        except:
            cr = False
        
        male_participants = participants.filter(gender='M')
        female_participants = participants.filter(gender = 'F')
        display_data = {
            'data': [
                college.name, cr, participants_count(male_participants),
                participants_count(female_participants), participants_count(participants),
                profile_stats(participants)
            ],
            'link' : [{
                'url': request.build_absolute_uri(reverse('pcradmin:stats_event_college', 
                kwargs={'e_id': event.id, 'c_id': college.id})),
                'title': 'View Participants'
            }]
        }
        rows.append(display_data)
    participants = Participant.objects.filter(id__in=[
        participant.id for participant in Participant.objects.filter(email_verified=True) if MainParticipation.objects.filter(participant = participant, event = event)
    ])
    male_participants = participants.filter(gender='M')
    female_participants = participants.filter(gender='F')
    display_data = {
        'data': [
            'Total', ' ', participants_count(male_participants),
            participants_count(female_participants), participants_count(participants),
            ' - - '
        ],
        'link' : [{'':''}]
    }
    rows.append(display_data)
    headings = [
        'College', 'CR Selected', 'Male', 'Female', 'Stats', 'Profile Status', 'View Details'
    ]
    title = 'CollegeWise Participants Stats for ' + event.name
    context = {
        'tables': [
            {'rows': rows, 'headings': headings, 'title':title}
        ]
    }
    return render(request, 'pcradmin/tables.html', context)

@staff_member_required
def stats_event_college(request, e_id, c_id):
    #e_id is event id and c_id is college id.
    event = get_object_or_404(MainEvent, id = e_id)
    college = get_object_or_404(College, id = c_id)
    participants1 = college.participant_set.filter(email_verified = True)
    participants = Participant.objects.filter(id__in=[
        participant.id for participant in Participant.objects.filter(email_verified=True) if MainParticipation.objects.filter(participant = participant, event = event)
    ])
    display_data = {
        'data': [
            participant.name, participant.college.name, get_cr_name(participant),
            participant.gender, participant.phone, participant.email, MainParticipation.objects.get(participant=p, event = event).pcr_approved,
            participant.paid or participant.curr_paid
        ],
        'link' : []
    }
    rows = [display_data for participant in participants]
    headings = ['Name', 'College', 'CR', 'Gender', 'Phone', 'Email', 'PCr Approval', 'Payment Status']
    title = "Participant's Stats for " + event.name + " from " + college.name
    context = {
        'tables': [
            {'rows': rows, 'headings': headings, 'title': title},   
        ]
    }
    return render(request, 'pcradmin/tables.html', context)

@staff_member_required
def master_stats(request):
    if request.method == 'POST':
        data = request.POST
        try:
            colleges = data.getlist('college')
        except:
            pass 
        try:
            events = data.getlist('event')
        except:
            pass
        if not colleges and not events:
            return redirect(request.META.get('HTTP_REFERRER'))
        if colleges[0]!='' and events[0]!='':
            participants = []
            for college_name in colleges:
                try:
                    college = College.objects.get(name=college_name)
                except:
                    continue
                for event_name in events:
                    try:
                        event = MainEvent.objects.get(name = event_name)
                    except:
                        continue
                    participations = MainParticipation.objects.filter(event=event)
                    participants+= Participant.objects.filter(id__in=[
                        participation.participant.id for participation in participations
                    ], college = college)
            display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, participant.pcr_approved,
                    participant.paid or participant.curr_paid
                ],
                'link' : []
            }
            rows = [display_data for participant in participants]
            headings = ['Name', 'College','Gender', 'Phone', 'Email', 'PCr Approval', 'Payment Status']
            event_names = ''
            for event_name in events:
                event_names += event_name + ', '
            event_names = event_names[:-2]
            #say "event1, event2, " is in event_names then last ', ' has to be removed before sending
            college_names = ''
            for college_name in colleges:
                college_names += college_name + ', '
            college_names = college_names[:-2]
            #same logic as up
            title = "Participants registered for %s event from %s college." %(event_names, college_names)

        elif events[0]!='':
            participants = []
            for event_name in events:
                try:
                    participations = MainParticipation.objects.filter(event = MainEvent.objects.get(name=event_name))
                except:
                    continue
                participants+= Participant.objects.filter(id__in=[
                        participation.participant.id for participation in participations
                    ])
            display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, participant.pcr_approved,
                    participant.paid or participant.curr_paid
                ],
                'link' : []
            }
            rows = [display_data for participant in participants]
            headings = ['Name', 'College','Gender', 'Phone', 'Email', 'PCr Approval', 'Payment Status']
            title = "Participants registered for %s event." %(event_name)

        else:
            participants = []
            for college_name in colleges:
                try:
                    college = College.objects.get(name=college_name)
                except:
                    continue
                participants += college.participant_set.all()
            display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, participant.pcr_approved,
                    participant.paid or participant.curr_paid
                ],
                'link' : []
            }
            rows = [display_data for participant in participants]
            headings = ['Name', 'College','Gender', 'Phone', 'Email', 'PCr Approval', 'Payment Status']
            title = "Participants registered from %s college." %(college_name)
        table = {
            'rows': rows,
            'headings': headings,
            'title': title,
        }
        context = {
            'tables': [table, ], 'colleges': colleges, 'events': events
        }
        events = MainEvent.objects.all()
        colleges = College.objects.all()
        return render(request, 'pcradmin/master_stats.html', context)
    events = MainEvent.objects.all()
    colleges = Colleges.objects.all()
    context = {
        'colleges': colleges, 'events': events
    }
    return render(request, 'pcradmin/master_stats.html', context)

########      HELPER FUNCTIONS     #######
def participants_count(participants):
	x1 = participants.count()
	if x1 == 0:
		return '- - - - '
	x2 = participants.filter(cr_approved=True, email_verified=True).count()
	x3=participants.filter(pcr_approved=True).count()
	x4=participants.filter(Q(paid=True)|Q(curr_paid=True)).count()
	x5 = participants.filter(pcr_final=True).count()
	return str(x1) + ' | ' + str(x2) + ' | ' + str(x3) + ' | ' + str(x4) + ' | ' + str(x5)

def get_cr_name(participant):
    return MainParticipation.objects.get(college=participant.college, is_cr=True).name

@login_required
def user_logout(request):
	logout(request)
	return redirect('pcradmin:index')

@staff_member_required
def contacts(request):
	return render(request, 'pcradmin/contacts.html')