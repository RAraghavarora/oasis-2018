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
from sendgrid.helpers.mail import *
import xlsxwriter
from time import gmtime, strftime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from oasis2018.keyconfig import *
import string
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




