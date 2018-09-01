from events.models import MainParticipation, MainEvent
from registrations.models import Participant,College,MainEvent
from django.shortcuts import render,redirect
import requests
from oasis2018 import keyconfig
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
import re
from registrations.views import send_grid
import sendgrid
from sendgrid.helpers.mail import *
from utils.registrations import *
from django.contrib import messages

def index(request):
    '''
    To register a new participant and send him a verification link
    '''
    if request.user.is_authenticated():
        user = request.user
        participant = Participant.objects.get(user=user)
        participation_set = MainParticipation.objects.filter(participant=participant)
        try:
            cr = Participant.objects.get(college=participant.college, is_cr=True)
        except:
            return JsonResponse({'status':0, 'message':'Sorry, you can\'t access this page.'})
        return render(request,'registrations/home.html',{'participant':participant,\
        'participations':participation_set,'cr':cr})
    
    if request.method=='GET':
        print("get request")
        colleges = College.objects.all()
        events = MainEvent.objects.all()
        return render(request, 'registrations/signup.html', {'college_list':colleges, 'event_list':events})
    
    if request.method=='POST':
        data = request.POST
        print(type(data.get('events[]')))
        recaptcha_response = data['g-recaptcha-response']
        data_1={
            'secret' : keyconfig.google_recaptcha_secret_key,
            'response' : recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data_1)
        
        result=r.json()
        if not result['success']:
            return JsonResponse({'status':0, 'message':'Invalid Recaptcha. Try Again'})
        email = data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return JsonResponse({'status':0, 'message':'Please enter a valid email address.'})
        try:
            Participant.objects.get(email=email)
            return JsonResponse({'status':0, 'message':'Email already registered.'})
        except:
            pass
        print("THIS:\t",data.getlist('events[]'))
        if len(data.getlist('events[]')) == 0:
            return JsonResponse({'status':0,'message':'Please select at least one event'})
        else:
            print("IN ELSE\n")
            participant = Participant()
            participant.name = str(data['name'])
            participant.gender = str(data['gender'])
            participant.city = str(data['city'])
            participant.email = str(data['email'])
            participant.college = College.objects.get(name = str(data['college']))
            participant.phone = int(data['phone'])
            if str(data['head_of_society']) == 'True':
                participant.head_of_society = True
            else:
                participant.head_of_society = False
            participant.year_of_study = int(data['year_of_study'])
            participant.save()
            print(data.getlist('events[]'))
            for key in data.getlist('events[]'):
                event = MainEvent.objects.get(id = int(key))
                MainParticipation.objects.create(event = event, participant = participant)
            participant.save()
            mail = send_grid.sendmail()
            send_to = str(request.POST["email"])
            name = str(request.POST['name'])
            to_email = Email(send_to)
            verify_email_url = str(request.build_absolute_uri(reverse("registrations:index"))) + 'email_confirm/' + \
            generate_email_token(Participant.objects.get(email=send_to)) + '/'
            print('Email url \t',verify_email_url)
            mail.body = mail.body%(name, verify_email_url)
            content = Content('text/html', mail.body)
            # 
            
            try:
                mail_1 = Mail(mail.from_email, mail.subject, to_email, content)
                response = send_grid.sg.client.mail.send.post(request_body = mail_1.get())
                # print(response)
            except Exception as e:
                print("\t",e)
                participant.delete()
                return JsonResponse({'status':0, 'message':'Error sending email. Please try again.'})
            
            message ="A confirmation link has been sent to {email}. Kindly click on it to verify your email address.".format(email=send_to)

            return JsonResponse({'status':1,'message':message})
        return HttpResponse('Redirect')

def home(request):
    '''
    Login page
    '''
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        
        if user is not None:
            if user.is_active:
                if not user.participant.email_verified:
                    message = "It seems you haven\'t verified your email yet. Please verify it as soon as possible to proceed. \
                    For any query, call the following members of the Department of Publications and Correspondence. Aditi Pandey: %s - pcr@bits-oasis.org .'%(get_pcr_number()), 'url':request.build_absolute_uri(reverse('registrations:home'))"
                    context = {'error_heading':'Email not verified','message' : message}
                login(request,user)
                return redirect('registrations:index')
            else:
                message="Your account is currently INACTIVE. To activate it, call the following members of the \
                Department of Publications and Correspondence. Aditi Pandey: %s - pcr@bits-bosm.org .'%(get_pcr_number()), 'url':request.build_absolute_uri(reverse('registrations:home'))"
                context = {'error_heading':'Email not verified','message':message}
                return render(request,'registrations/message.html',context)
        else:
            messages.warning(request,'Invalid login credentials')
            return redirect(request.META.get('HTTP_REFERER'))
    
    elif request.method == 'GET':
        return render(request,'registrations/login.html')
        


def email_confirm(request,token):
    member = authenticate_email_token(token)
    print("EMAIL CONFIRM")
    if member:
        context = {
        'error_heading': 'Email verified',
        'message': 'Your email has been verified. Please wait for further correspondence from the Department of PCr, BITS, Pilani',
        'url':'https://bits-oasis.org'
        }
    else:
        context = {
        'error_heading': "Invalid Token",
        'message': "Sorry!  Email couldn't be verified. Please try again.",
        'url':'https://bits-oasis.org'
        }
    return render(request, 'registrations/message.html', context)
