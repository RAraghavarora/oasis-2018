from events.models import MainParticipation, MainEvent
from registrations.models import Participant,College,MainEvent
from django.shortcuts import render
import requests
from oasis2018 import keyconfig
from django.http import HttpResponse,JsonResponse
import re

def index(request):
    if request.user.is_authenticated():
        user = request.user
        participant = Participant.objects.get(user=user)
        participation_set = MainParticipation.objects.filter(participant=participant)
        cr = Participant.objects.get(college=participant.college, is_cr=True)
        return render(request,'registrations/home.html',{'participant':participant,\
        'participations':participation_set,'cr':cr})
    
    if request.method=='GET':
        print("get request")
        colleges = College.objects.all()
        events = MainEvent.objects.all()
        return render(request, 'registrations/signup.html', {'college_list':colleges, 'event_list':events})
    
    if request.method=='POST':
        data = request.POST
        
        recaptcha_response = data['g-recaptcha-response']
        data_1={
            'secret' : keyconfig.google_recaptcha_secret_key,
            'response' : recaptcha_response
        }
        print(data_1)
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data_1)
        
        result=r.json()
        print('***\n',result)
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
        print(data.getlist('events[]'))
        return HttpResponse('Redirect')

def abc(request):
    return HttpResponseRedirect('<h1>HELLO </h1>')