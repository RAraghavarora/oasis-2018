from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registrations.models import Participant
from events.models import MainParticipation
from django.urls import reverse
from django.shortcuts import render
import string
from random import choice
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
from . import send_grid
import sendgrid
from sendgrid.helpers.mail import *
from utils.registrations import *
from django.http import HttpResponse

@login_required
def approve(request):
    '''
    Page where CR will approve the participations of his college
    '''
    user = request.user
    participant = Participant.objects.get(user=user)
    if not participant.is_cr:
        context = {
            'error_heading':'Invalid Access',
            'message':'Sorry, you are not an approved college representative.',
            'url':request.build_absolute_uri(reverse('registrations:home'))
        }
        return render(request, 'registrations/message.html', context)
    approved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=True)
    disapproved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=False,email_verified=True)
    for person in disapproved_list:
        print(person.participant,'\t',person.participant.email)
    
    if request.method == 'GET':
        context={'approved_list':approved_list,'disapproved_list':disapproved_list,'participant':participant}
        return render(request, 'registrations/cr_approval.html',context)
    elif request.method == 'POST':
        data = request.POST
        if data['action'] == 'approve':
            try:
                parts_id = data.getlist('parts_id')
                # parts_id is the list of all the id's cr chooses
            except:
                #goodbye
                return redirect(request.META.get('HTTP_REFERER'))
            for id in parts_id:
                participation = MainParticipation.objects.get(id=id,participant__college=participant.college)
                print("participation is \t",participation)
                participation.cr_approved = True
                participation.save()
                participant_1 = participation.participant
                participant.cr_approved=True
                participant_1.save()
                print(participant_1.user)
                if participant_1.user is not None:
                    user = participant_1.user
                    if not user.is_active:
                        user.is_active=True
                        user.save
                else:
                    username = participant.name.split(' ')[0] + str(participant_1.id)
                    password = ''.join(choice(chars) for i in range(8))
                    print(password)
                    user = User.objects.create_user(username=username, password=password)
                    participant_1.user=user
                    participant_1.save()
                    email_class = send_grid.cr_approved()
                    name = participant_1.name
                    send_to = participant_1.email
                    login_url = str(request.build_absolute_uri(reverse('registrations:home')))
                    body = email_class.body%(name,login_url,username,password,get_pcr_number())
                    to_email=Email(send_to)
                    content = Content('text/html', body)
                    try:
                        mail = Mail(email_class.from_email,email_class.subject,to_email,content)
                        response = send_grid.sg.client.mail.send.post(request_body = mail.get())
                        print("EMAIL SENT")
                    except Exception as e :
                        print(e)
                        participant_1.user = None
                        participant_1.save()
                        user.delete()
                        participation.cr_approved = False
                        participation.save()
                        context = {
                        'status': 0,
                        'error_heading': "Error sending mail",
                        'message': "Sorry! Error in sending email. Please try again.",
                        }
                        return render(request, 'registrations/message.html', context)
                    
                    context = {
                        'error_heading':"Emails sent",
                        'message' : "Login credentials have been mailed to the corresponding new participants."
                    }
                    return render(request, 'registrations/message.html', context)

        if 'disapprove' == data['action']:
            try:
                parts_id = data.getlist('parts_id')
            except:
                return redirect(request.META.get('HTTP_REFERER'))
            for part_id in parts_id:
                participation = MainParticipation.objects.get(id=part_id, participant__college=participant.college)
                participation.cr_approved = False
                participation.pcr_approved = False
                participation.save()
                participant_1 = participation.participant
                if all(not i.cr_approved for i in participant_1.mainparticipation_set.all()):
                    participant_1.cr_approved = False
                    participant_1.save()
        approved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=True)
        disapproved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=False)
        return render(request, 'registrations/cr_approval.html', {'approved_list':approved_list, 'disapproved_list':disapproved_list, 'participant':participant})

@login_required
def participant_details(request,p_id):
    '''
    For the cr to see the details of any participant from his college
    '''
    user = request.user
    participant = Participant.objects.get(user=user)
    if not participant.is_cr:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You are not an approved college representative.",
        'url':request.build_absolute_uri(reverse('registrations:index'))
        }
        return render(request, 'registrations/message.html', context)
    get_part = Participant.objects.get(id=p_id)
    if not get_part.college == participant.college:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You do not have access to these details.",
        'url':request.build_absolute_uri(reverse('registrations:index'))
        }
        return render(request, 'registrations/message.html', context)
    participation_list = MainParticipation.objects.filter(participant=get_part)
    return render(request, 'registrations/profile.html', {'get_part':get_part, 'participations':participation_list, 'participant':participant})

@login_required
def get_profile_card_cr(request, p_id):
    user = request.user
    # print("******")
    participant = Participant.objects.get(user=user)
    if not participant.is_cr:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You are not an approved college representative.",
        'url':request.build_absolute_uri(reverse('registrations:index'))
        }
        return render(request, 'registrations/message.html', context)
    get_part = Participant.objects.get(id=p_id)
    if not get_part.college == participant.college:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You do not have access to these details.",
        'url':request.build_absolute_uri(reverse('registrations:index'))
        }
        return render(request, 'registrations/message.html', context)
    if not get_part.firewallz_passed:
        context = {
                'error_heading': "Invalid Access",
                'message': "Please pass firewallz booth at BITS to access this page.",
                'url':request.build_absolute_uri(reverse('registrations:index'))
                }
        return render(request, 'registrations/message.html', context)
    participation_set = MainParticipation.objects.filter(participant=get_part, pcr_approved=True)
    events = ''
    for participation in participation_set:
        events += participation.event.name + ', '
    print(events)
    events = events[:-2]
    return render(request, 'registrations/profile_card.html', {'participant':get_part, 'events':events,})