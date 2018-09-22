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
from reportlab.platypus.tables import Table
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle,Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from oasis2018.keyconfig import *
import string
from django.contrib import messages
from random import choice
from utils.registrations import *
API_KEY='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' #my api 

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
        try:
            if request.META["CONTENT_TYPE"] == "application/json":
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
        except:
            data = request.POST
        try:
            part_id=data['data']
        except:
            messages.warning(request,'Select a participant')
            return redirect(request.META.get('HTTP_REFERER'))
        

        if data['submit']=='delete':
            part=Participant.objects.get(id=part_id)
            user=part.user
            #user.delete()
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
            #encoded = gen_barcode(part)
            print("dsd")

            #Barcode generation here left for now. To be discussed if only QR or not
            part.save()
            user=part.user
            if not user==None:
                messages.warning(request,'College Representative already selected.')
                return redirect(request.META.get('HTTP_REFERER'))
            if user==None:
                username=part.name.split()[0]+str(part_id)
                length=8
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                password = ''.join(choice(chars) for _ in range(length))
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
			""" %(part.name,str(request.build_absolute_uri(reverse('registrations:home'))),username, password,get_pcr_number() ) #get_pcr_number()
            subject = 'College Representative for Oasis'
            from_email = Email('register@bits-oasis.org')
            to_email = Email(part.email)
            content = Content('text/html', body)
            sg = sendgrid.SendGridAPIClient(apikey=API_KEY) #Email validation with my email for now
            try:
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
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
    parts = [{'data':[part.name, part.phone, part.email, part.gender, part.pcr_approved, part.head_of_society, part.year_of_study, event_list(part), how_much_paid(part)], "id":part.id,} for part in participants]
    
    return render(request, 'pcradmin/college_rep.html',{'college':college, 'parts':parts, 'cr':cr})


###HELPER FUNCTIONS WRT TO THE ABOVE VIEW###
def event_list(part):
    events=''
    for participation in MainParticipation.objects.filter(participant=part):
        events+=participation.event.name +','
    events=events[:-2]
    return events

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
                participant=participation.participant
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
def verify_profile(request,part_id):
    part=Participant.objects.get(id=part_id)
    if request.method=='POST':
        try:
            data=(request.POST)
            data1 = dict(data)
            print(data)
        except:
            messages.warning(request,'Please select an event')
            return redirect(request.META.get('HTTP_REFERER'))
        if data['submit']=='confirm':
            MainParticipation.objects.filter(id__in=data1['data'],cr_approved=True).update(pcr_approved=True)
            part.pcr_approved=True
            message = part.name + '\'s Profile Verified'
        elif data['submit']=='unconfirm':
            MainParticipation.objects.filter(id__in=data1['data'],cr_approved=True).update(pcr_approved=True)
            message='Events succesfully unconfirmed'
            not_pcr_approved_particpants=[not participant.pcr_approved for participant in MainParticipation.objects.filter(particpant=part)]
            if all(not_pcr_approved_particpants):       
                part.pcr_approved=False
                message += ' and ' + part.name + '\'sprofile is uncofirmed'
                #Look into the above functionality
        part.save()
        messages.success(request, "Done")
        return redirect(reverse('pcradmin:select_college_rep', kwargs={'id':part.college.id}))
        '''try:
		profile_url = part.profile_pic.url
		docs_url = part.verify_docs.url
	except:
		message = part.name + '\'s Profile not complete yet.'
		messages.warning(request, message)
		return redirect(request.META.get('HTTP_REFERER'))'''
    participations=part.mainparticipation_set.all()
    events_confirmed = [{'event':p.event, 'id':p.id} for p in participations.filter(pcr_approved=True)]
    events_unconfirmed = [{'event':p.event, 'id':p.id} for p in participations.filter(pcr_approved=False)]
    return render(request, 'pcradmin/verify_profile.html',
	{ 'part':part, 'confirmed':events_confirmed, 'unconfirmed':events_unconfirmed})
        
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
    return render(request,'pcradmin/edit_participant.html',{'participant':participant})




#################################### STATS ##########################################     


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
        rows = []
        for participant in Participant.objects.filter(Q(pcr_approved=True), Q(paid=True)|Q(curr_paid=True)):
            display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, get_payment_status(participant),
                    get_event_string(participant)
                ],
                'link' : []
            }
            rows.append(display_data)
        headings = ['Name', 'College', 'Gender', 'Phone', 'Email', 'Payment Made', 'Events']
        title = "Participant's Payment Status"
        context = {
            'tables': [
                {'rows': rows, 'headings': headings, 'title': title},   
            ]
        }
        return render(request, 'pcradmin/tables.html', context)
def get_payment_status(part):
	if part.paid or part.curr_paid:
		if part.controlz_paid or part.curr_controlz_paid:
			return 950
		else:
			return 300
	else:
		return 0
def get_event_string(participant):
    participation_set = MainParticipation.objects.filter(participant=participant, pcr_approved=True)
    events = ''
    for participation in participation_set:
        events += participation.event.name + ', '
    events = events[:-2]
    return events

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
    rows=[]
    for participant in participants:
        
        display_data = {
            'data': [
                participant.name, participant.college.name, get_cr_name(participant),
                participant.gender, participant.phone, participant.email, MainParticipation.objects.get(participant=p, event = event).pcr_approved,
                participant.paid or participant.curr_paid
            ],
            'link' : []
        }
        rows.append(display_data)
        
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
    events = MainEvent.objects.all()
    colleges = College.objects.all()
    context = {'events':events, 'colleges':colleges}
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
        rows = []
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
            for participant in participants:
                display_data = {
                'data': [
                    participant.name, participant.college.name, participant.gender,
                    participant.phone, participant.email, participant.pcr_approved,
                    participant.paid or participant.curr_paid
                ],
                'link' : []
                }
                rows.append(display_data)
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
            for participant in participants:
                display_data = {
                    'data': [
                        participant.name, participant.college.name, participant.gender,
                        participant.phone, participant.email, participant.pcr_approved,
                        participant.paid or participant.curr_paid
                    ],
                    'link' : []
                }
                rows.append(display_data)
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
            for participant in participants:
                display_data = {
                    'data': [
                        participant.name, participant.college.name, participant.gender,
                        participant.phone, participant.email, participant.pcr_approved,
                        participant.paid or participant.curr_paid
                    ],
                    'link' : []
                }
                rows.append(display_data)
            headings = ['Name', 'College','Gender', 'Phone', 'Email', 'PCr Approval', 'Payment Status']
            title = "Participants registered from %s college." %(college_name)
        table = {
            'rows': rows,
            'headings': headings,
            'title': title,
        }
        context['tables'] = [table, ]

        # context = {
        #     'tables': [table, ], 'colleges': colleges, 'events': events
        # }
        
        return render(request, 'pcradmin/master_stats.html', context)
    # events = MainEvent.objects.all()
    # colleges = College.objects.all()
    # context = {
    #     'colleges': colleges, 'events': events
    # }
    return render(request, 'pcradmin/master_stats.html', context)

@staff_member_required
def view_final(request):
	rows = [{'data':[college.name,college.participant_set.filter(pcr_approved=True, pcr_final=True).count(),college.participant_set.filter(pcr_approved=True).count()],'link':[{'title':'Select', 'url':reverse('pcradmin:final_confirmation', kwargs={'c_id':college.id})}] } for college in College.objects.all()]
	tables = [{'title':'List of Colleges', 'rows':rows, 'headings':['College', 'Finalised','Total Approved', 'Select']}]
	return render(request, 'pcradmin/tables.html', {'tables':tables})

@staff_member_required
def final_confirmation(request, c_id):
	college = College.objects.get(id=c_id)
	if request.method == 'POST':
		data = request.POST
		try:
			id_list = data.getlist('data')
		except:
			messages.warning(request,'Select a Participant')
			return redirect(request.META.get('HTTP_REFERER'))
		if not id_list:
			messages.warning(request,'Select a Participant')
			return redirect(request.META.get('HTTP_REFERER'))
		parts = Participant.objects.filter(id__in=id_list)
		if data['action'] == 'approve':
			emailgroup = EmailGroup.objects.create()
			for part in parts:
				part.email_group = emailgroup
				part.save()
			return redirect(reverse('pcradmin:final_email', kwargs = {'eg_id':emailgroup.id}))
		elif data['action'] == 'disapprove':
			for part in parts:
				part.email_group = None
				part.pcr_final = False
				part.save()
	parts = college.participant_set.filter(pcr_approved=True, pcr_final=False)
	parts_final = college.participant_set.filter(pcr_approved=True,pcr_final=True)
	return render(request, 'pcradmin/final_confirmation.html', {'parts':parts, 'college':college, 'parts_final':parts_final})
   
@staff_member_required
def final_email(request, eg_id):
	email_group = EmailGroup.objects.get(id=eg_id)
	parts = email_group.participant_set.all()
	college = parts[0].college
	return render(request, 'pcradmin/final_email.html', {'parts':parts, 'group':email_group, 'college':college})

@staff_member_required
def final_email_send(request, eg_id):
    email_group = EmailGroup.objects.get(id = eg_id)
    participants = email_group.participant_set.all()
    college = participants[0].college
    try:
        _dir = '/root/live/oasis/backend/resources/oasis2018/'
        doc_name = _dir + 'final_list.pdf'
        pdf = create_final_pdf(eg_id, doc_name, _dir)
    except:
        _dir = '/home/raghav/Downloads/'
        doc_name = _dir + 'final_list.pdf'
        pdf = create_final_pdf(eg_id, doc_name, _dir)
    
    #sendgrid email sending code

    import base64
    with open(pdf, "rb") as output_pdf:
        encoded_string1 = base64.b64encode(output_pdf.read())
    attachment = Attachment()
    attachment.content = encoded_string1.decode()
    attachment.filename = 'Confirmed_Participants.pdf'

    # with open(_dir+'Instructions to Participants', "rb") as output_doc:
    #     encoded_string2 = base64.b64encode(output_doc.read()) Instruction to participants
    #attachment_1 = Attachment()
    #attachment_1.content = encoded_string2
    #attachment_1.filename = 'Instructions to Participants.docx'
    subject = 'Final Confirmation for Oasis'
    from_email = Email('register@bits-oasis.org')
    sg = sendgrid.SendGridAPIClient(apikey=API_KEY)
    for participant in participants:
        to_email = Email(participant.email)
        body = """<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet"> 
			<center><img src="http://bits-oasis.org/2018/static/registrations/img/logo.png" height="150px" width="150px"></center>
			<pre style="font-family:Roboto,sans-serif">
Hello %s!
Greetings from BITS Pilani!

It gives me immense pleasure in inviting your institute to the 48th edition of OASIS, the annual cultural fest of Birla Institute of Technology & Science, Pilani, India. This year, OASIS will be held from October 31st to November 4th.             
           
This is to confirm your participation at OASIS '18.
We would be really happy to see your college represented at our fest.

We look forward to seeing you at OASIS 2018.
A new link would be active in your OASIS '18 account once you clear the Firewallz booth at BITS with the access to your exclusive profile card.
<b>IT IS COMPULSORY FOR YOU TO BRING A VALID IDENTITY CARD, WITHOUT WHICH YOU WON'T BE ALLOWED TO ENTER THE PREMISES.</b>
PFA A list of participants from your college.

Regards,
StuCCAn (Head)
Dept. of Publications & Correspondence, OASIS 2018
BITS Pilani
%s
pcr@bits-oasis.org

<b>Please reply to this email with number of people, if you require conveyance to or from Loharu and the timings for it.</b>
</pre>
			""" %(participant.name,get_pcr_number()) 
        content = Content('text/html', body)
        try:
            mail = Mail(from_email, subject, to_email, content)
            mail.add_attachment(attachment)
            #mail.add_attachment(attachment_1)
            response = sg.client.mail.send.post(request_body=mail.get())
            print('done')
            messages.warning(request, 'Email sent to ', participant.name)
            participant.pcr_final = True
            # ems_code = str(participant.college.id).rjust(3, '0')+str(participant.id).rjust(4,'0')
            # participant.ems_code = ems_code

            #finally
            participant.save()
            # if not participant.is_cr:
            #     encoded=gen_barcode(participant)
            #     participant.save()

        # except Exception, e: does not work in py3
        except Exception as e:
            print(str(e))
            messages.warning(request, 'Error sending email')
    return redirect(reverse('pcradmin:final_confirmation', kwargs={'c_id': college.id}))

@staff_member_required
def download_pdf(request, eg_id):
    try:
        _dir = '/root/live/oasis/backend/resources/oasis2018/'
        doc_name = _dir + 'final_list.pdf'
        pdf_1 = create_final_pdf(eg_id, doc_name, _dir)

    except:
        _dir = '/home/raghav/Downloads/'
        doc_name = _dir + 'final_list.pdf'
        pdf_1 = create_final_pdf(eg_id, doc_name, _dir)
    pdf = open(pdf_1, 'rb')
    response = HttpResponse(content_type='application/pdf', content=pdf)
    response['Content-Disposition'] = 'attachment; filename="final_list.pdf"'
    return response

#not much idea of the functions of reportlab... 
def create_final_pdf(eg_id, response, _dir):
    logo="/home/raghav/dvm/oasis-2018/pcradmin/static/pcradmin/images/Oasis-Logo.png"
    im=Image(logo,1*inch,1*inch)
    email_group = EmailGroup.objects.get(id=eg_id)
    elements = []
    doc = SimpleDocTemplate(response, pagesize=letter)
    data = [('Name', 'Events', 'Payment')]
    for part in email_group.participant_set.all():
        events = ''
        for participation in MainParticipation.objects.filter(participant=part, pcr_approved=True):
            events += participation.event.name + ', '
        events = events[:-2]
        amount = how_much_paid(part)
        data.append((part.name, events, amount))
    
    table_with_style = Table(data, [3 * inch, 1.5 * inch, inch])

    table_with_style.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, 0), 0.25, colors.green),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ]))


    doc.build([Spacer(1, 0.5 * inch),table_with_style,im])
    watermark_name = _dir + 'Unused.pdf' #Change the watermark
    output_file = PdfFileWriter()
    input_file = PdfFileReader(open(response, "rb"))
    page_count = input_file.getNumPages()
    for page_number in range(page_count):
        watermark = PdfFileReader(open(watermark_name, "rb"))
        input_page = watermark.getPage(0)
        input_page.mergePage(input_file.getPage(page_number))
        output_file.addPage(input_page)
    output_name = _dir +'final_pdf.pdf'
    with open(output_name, "wb") as outputStream:
        output_file.write(outputStream)
    return output_name


########      HELPER FUNCTIONS     #######
# some helper fns are there along with the view code  they are limited only to that view
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

def profile_stats(parts):
    #What this function does is:
    # its input is a list of participants and this function returns 
    # number of profiles fully completed and number of participants approved by pcr
    x = parts.filter(pcr_approved = True).count()
    # y = 0

    # for part in parts:
    #     if is_profile_complete(part):
    #         y+= 1

    return str(x)