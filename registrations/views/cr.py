from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registrations.models import Participant, PaymentGroup
from events.models import MainParticipation
from django.urls import reverse
from django.shortcuts import render,redirect
import string
from random import choice
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
from . import send_grid
import sendgrid
from sendgrid.helpers.mail import *
from utils.registrations import *
from django.http import HttpResponse, HttpResponseRedirect
from instamojo_wrapper import Instamojo
from oasis2018.settings_config import keyconfig
import requests
import json


api = Instamojo(api_key=keyconfig.INSTA_API_KEY_test, auth_token=keyconfig.AUTH_TOKEN_test, endpoint='https://test.instamojo.com/api/1.1/') #when in development


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

    # approved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=True)
    # disapproved_list = MainParticipation.objects.filter(participant__college = participant.college, cr_approved=False,participant__email_verified=True)

    #participant is the one who is logged in. Candidate is the one chosen by the CR(participant)
    approved_list= Participant.objects.filter(college = participant.college, cr_approved=True,email_verified=True)
    disapproved_list = Participant.objects.filter(college = participant.college, cr_approved=False,email_verified=True)
    
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
                try:
                    candidate = Participant.objects.get(id=id,college=participant.college)
                except:
                    context = {
                        'error_heading':'Error Occured',
                        'message':'Sorry, you cannot perform this action',
                        'url':request.build_absolute_uri(reverse('registrations:home'))
                    }
                    return render(request, 'registrations/message.html', context)
                participations = MainParticipation.objects.filter(participant=candidate)
                participations.update(cr_approved=True)
                candidate.cr_approved=True
                candidate.save()
                if candidate.user is not None:
                    user = candidate.user
                    if not user.is_active:
                        user.is_active=True
                        user.save()
                else:
                    username = candidate.name.split(' ')[0] + str(candidate.id)
                    password = ''.join(choice(chars) for i in range(8))
                    print(password)
                    user = User.objects.create_user(username=username, password=password)
                    candidate.user=user
                    candidate.save()
                    email_class = send_grid.cr_approved()
                    name = candidate.name
                    send_to = candidate.email
                    login_url = str(request.build_absolute_uri(reverse('registrations:home')))
                    body = email_class.body%(name,login_url,username,password,get_pcr_number())
                    to_email=Email(send_to)
                    content = Content('text/html', body)
                    try:
                        mail = Mail(email_class.from_email,email_class.subject,to_email,content)
                        response = send_grid.sg.client.mail.send.post(request_body = mail.get())
                        if response.status_code%100!=2:
                            raise Exception
                        print("EMAIL SENT")
                    except Exception as e :
                        print(e)
                        candidate.user = None
                        candidate.save()
                        user.delete()
                        participations.update(cr_approved=False)
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
                candidate = Participant.objects.get(id=part_id)
                participations = MainParticipation.objects.filter(participant=candidate)
                participations.update(cr_approved=False,pcr_approved=False)
                # participant_1 = participation.participant
                # if all(not i.cr_approved for i in participant_1.mainparticipation_set.all()):
                #     participant_1.cr_approved = False
                #     participant_1.save()
                candidate.cr_approved=False
                try:
                    user = candidate.user
                    user.is_active=False
                    user.save()
                except:
                    pass
                candidate.save()
        approved_list = Participant.objects.filter(college = participant.college, cr_approved=True,email_verified=True)
        disapproved_list = Participant.objects.filter(college = participant.college, cr_approved=False, email_verified=True)
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
        'url':request.build_absolute_uri(reverse('registrations:home'))
        }
        return render(request, 'registrations/message.html', context)
    get_part = Participant.objects.get(id=p_id)
    if not get_part.college == participant.college:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You do not have access to these details.",
        'url':request.build_absolute_uri(reverse('registrations:home'))
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
        'url':request.build_absolute_uri(reverse('registrations:home'))
        }
        return render(request, 'registrations/message.html', context)
    get_part = Participant.objects.get(id=p_id)
    if not get_part.college == participant.college:
        context = {
        'error_heading': "Invalid Access",
        'message': "Sorry! You do not have access to these details.",
        'url':request.build_absolute_uri(reverse('registrations:home'))
        }
        return render(request, 'registrations/message.html', context)
    if not get_part.firewallz_passed:
        context = {
                'error_heading': "Invalid Access",
                'message': "Please pass firewallz booth at BITS to access this page.",
                'url':request.build_absolute_uri(reverse('registrations:home'))
                }
        return render(request, 'registrations/message.html', context)
    participation_set = MainParticipation.objects.filter(participant=get_part, pcr_approved=True)
    events = ''
    for participation in participation_set:
        events += participation.event.name + ', '
    print(events)
    events = events[:-2]
    return render(request, 'registrations/profile_card.html', {'participant':get_part, 'events':events,})

@login_required
def cr_stats(request):
    participant = Participant.objects.get(user=request.user)
    college = participant.college
    approved_participants = Participant.objects.filter(college = college, cr_approved=True)
    disapproved_participants = Participant.objects.filter(college = college, cr_approved=False)

    context = {'approved_list':approved_participants,'disapproved_list':disapproved_participants}

    return render(request, 'registrations/stats.html',context)

def pcr_stats(request,p_id):
    candidate = Participant.objects.get(id=p_id)
    participations = MainParticipation.objects.filter(participant = candidate)
    
    context = {'participations':participations,'candidate_name':candidate.name.title()}

    return render(request, 'registrations/pcrstats.html',context)

@login_required
def payment(request):
    user = request.user
    participant = Participant.objects.get(user=user)
    if not participant.is_cr:
        context = {
        'status': 0,
        'error_heading': "Invalid Access",
        'message': "Sorry! You are not an approved college representative.",
        }
        return render(request, 'registrations/message.html', context)
    if request.method == 'POST':
        data = request.POST
        print("DATA=\n",data)
        try:
            key = int(data['key'])
            part_list = data.getlist('part_list')
            print("LEN=",len(part_list))
            if len(part_list)==0:
                messages.warning(request,'Error:Please select participants')
                return redirect(request.META.get('HTTP_REFERER'))
        except:
            return redirect(request.META.get('HTTP_REFERER'))
        if key == 1:
            amount = 300
            programId = 9381
        elif key == 2:
            amount = 1000
            programId = 9183
        elif key == 3:
            amount = 700
            programId = 9382
        part_list = Participant.objects.filter(id__in=data.getlist('part_list'), pcr_approved=True)
        # print(part_list)
        group = PaymentGroup()
        total_amount = amount*len(part_list)
        # print(total_amount)
        group.amount_paid = total_amount
        group.save()
        # print(group)
        attendees = []
        for part in part_list:
            dataa={'name':part.name, 'email':part.email, 'phone':part.phone, 'college':part.college.name}
            attendees+=[dataa]
            part.payment_group = group
            part.save()
        # print(attendees)
        name = participant.name
        email = participant.email
        phone = participant.phone
        college = participant.college
        purpose = 'Payment ' + str(group.id)

        # response = api.payment_request_create(
        #     buyer_name = name,
        #     email = email,
        #     phone = phone,
        #     amount = group.amount_paid,
        #     purpose = purpose,
        #     redirect_url = request.build_absolute_uri(reverse("registrations:payment_response"))
        #     )
        login_url = 'https://www.thecollegefever.com/v1/auth/basiclogin'
        headers = {'Content-Type': 'application/json'}
        login_data = {"email":"webmaster@bits-oasis.org","password":"Ashujain@1997"} 
        # try:
        login_response = requests.post(url=login_url, headers=headers, data=json.dumps(login_data))
        status_code = login_response.status_code
        # if status_code==200:
        json_ob = json.loads(login_response.text)
        session = json_ob['sessionId']

        book_data = {
            "eventId":4148,
            "totalFare":total_amount,
            "addExtra":0,
            "attendingEvents":[
                {
                    "programId":programId,
                    "programName":"Oasis 2018 Registrations",
                    "subProgramName":"Registration",
                    "fare":amount,
                    "attendees":attendees
                }
            ]
        }
        book_url = 'https://www.thecollegefever.com/v1/booking/bookticket'
        cookies = {'auth':session}
        book_response = requests.post(url=book_url, headers=headers, data=json.dumps(book_data), cookies=cookies)
        status_code_2 = book_response.status_code
        # if status_code_2==200:
        json_ob_2 = json.loads(book_response.text)
        # print(json_ob_2)
        
        page = json_ob_2['pgUrl']
        # print(page)
        # response = api.payment_request_create(
        #     amount = amount,
        #     purpose = purpose,
        #     # send_email = False,
        #     buyer_name = name,
        #     email = email,
        #     phone = phone,
        #     redirect_url = request.build_absolute_uri(reverse("registrations:payment_response"))
        # )
        # print(response)
        # print(response['payment_request']['status'])
        # print(email)
        # print(response['payment_request']['longurl'])
        
        try:
            # url = response['payment_request']['longurl']
            url = page
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            context = {
            'error_heading': "Payment error",
            'message': "An error was encountered while processing the request. Please contact PCr, BITS, Pilani.",
            'url':request.build_absolute_uri(reverse('registrations:make_payment'))
            }
            return render(request, 'registrations/message.html')
        
    else:
        participant_list = Participant.objects.filter(college=participant.college,paid=False, pcr_approved=True)
        prereg_list = Participant.objects.filter(college=participant.college, paid=True, controlz_paid=False)
        paid_list = Participant.objects.filter(college=participant.college, paid=True, controlz_paid=True)
        return render(request, 'registrations/cr_payment.html', {'participant_list':participant_list, 'participant':participant, 'prereg_list':prereg_list, 'paid_list':paid_list})

@login_required
def chor_approve(request):
    '''
    Page where CR will approve the choreographers of his college
    '''
    user = request.user
    participant = Participant.objects.get(user=user)
    approved_list= Participant.objects.filter(college = participant.college, cr_approved=True,email_verified=True, is_chor=True)
    disapproved_list = Participant.objects.filter(college = participant.college, cr_approved=False,email_verified=True,is_chor=True)
    
    if request.method == 'GET':
        context={'approved_list':approved_list,'disapproved_list':disapproved_list,'participant':participant}
        return render(request, 'registrations/chor_approval.html',context)
    
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
                try:
                    candidate = Participant.objects.get(id=id,college=participant.college)
                except:
                    context = {
                        'error_heading':'Error Occured',
                        'message':'Sorry, you cannot perform this action',
                        'url':request.build_absolute_uri(reverse('registrations:home'))
                    }
                    return render(request, 'registrations/message.html', context)
                participations = MainParticipation.objects.filter(participant=candidate)
                participations.update(cr_approved=True)
                candidate.cr_approved=True
                candidate.save()
                if candidate.user is not None:
                    user = candidate.user
                    if not user.is_active:
                        user.is_active=True
                        user.save()
                else:
                    username = candidate.name.split(' ')[0] + str(candidate.id)
                    password = ''.join(choice(chars) for i in range(8))
                    print(password)
                    user = User.objects.create_user(username=username, password=password)
                    candidate.user=user
                    candidate.save()
                    email_class = send_grid.cr_approved()
                    name = candidate.name
                    send_to = candidate.email
                    login_url = str(request.build_absolute_uri(reverse('registrations:home')))
                    body = email_class.body%(name,login_url,username,password,get_pcr_number())
                    to_email=Email(send_to)
                    content = Content('text/html', body)
                    try:
                        mail = Mail(email_class.from_email,email_class.subject,to_email,content)
                        response = send_grid.sg.client.mail.send.post(request_body = mail.get())
                        if response.status_code%100!=2:
                            raise Exception
                        print("EMAIL SENT")
                    except Exception as e :
                        print(e)
                        candidate.user = None
                        candidate.save()
                        user.delete()
                        participations.update(cr_approved=False)
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
                candidate = Participant.objects.get(id=part_id)
                participations = MainParticipation.objects.filter(participant=candidate)
                participations.update(cr_approved=False,pcr_approved=False)
                # participant_1 = participation.participant
                # if all(not i.cr_approved for i in participant_1.mainparticipation_set.all()):
                #     participant_1.cr_approved = False
                #     participant_1.save()
                candidate.cr_approved=False
                try:
                    user = candidate.user
                    user.is_active = False
                    user.save()
                except:
                    pass
                candidate.save()
        approved_list = Participant.objects.filter(college = participant.college, cr_approved=True,email_verified=True,is_chor=True)
        disapproved_list = Participant.objects.filter(college = participant.college, cr_approved=False, email_verified=True,is_chor=True)
        return render(request, 'registrations/chor_approval.html', {'approved_list':approved_list, 'disapproved_list':disapproved_list, 'participant':participant})

