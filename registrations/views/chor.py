from registrations.models import Participant, College
from events.models import MainEvent
from django.shortcuts import render
import re
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from utils.registrations import *
from registrations.models import MainParticipation
from . import send_grid
import sendgrid
from sendgrid.helpers.mail import *
from django.urls import reverse


def register(request):
	'''
	To register a choreographer
	'''
	if request.method=='GET':
		colleges = College.objects.all()
		events = MainEvent.objects.all()
		context = {'colleges':colleges,'events':events}
		return render(request,'registrations/chor_register.html',context)
	elif request.method=='POST':
		data = request.POST
		# print(data)
		if len(data['phone'])!=10:
			return JsonResponse({'status':0,'message':'Please enter a valid contact number.'})
		try:
			int(data['phone'])
		except:
			return JsonResponse({'status':0,'message':'Please enter a valid contact number.'})            
		email = data['email']
		if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return JsonResponse({'status':0, 'message':'Please enter a valid email address.'})

		try:
			Participant.objects.get(email=email)
			return JsonResponse({'status':0, 'message':'Email already registered.'})
		except:
			pass
		if len(data.getlist('events[]')) == 0:
			return JsonResponse({'status':0,'message':'Please select at least one event'})

		try:
			participant = Participant()
			name = ' '.join(str(data['name']).strip().split())
			participant.name = name
			participant.gender = str(data['gender'])
			participant.city = str(data['city'])
			participant.email = str(data['email'])

			try:
				participant.college = College.objects.get(name = data['college'])
			except:
				return JsonResponse({'status':0,'message':'Invalid College'})
			participant.phone = int(data['phone'])
		    
		    
		except KeyError as missing_data:
		    response = JsonResponse({'message':'Data is Missing: {}'.format(missing_data), 'x_status': 4})
		    # response.delete_cookie('sessionid')
		    return response
		participant.is_chor=True
		participant.save()
		print(data.getlist('events[]'))

		for key in data.getlist('events[]'):
			event = MainEvent.objects.get(id=int(key))
			MainParticipation.objects.create(event = event, participant = participant)
		participant.save()

		mail = send_grid.chor()
		send_to = str(data["email"])
		name = str(data['name'])
		to_email = Email(send_to)
		verify_email_url = str(request.build_absolute_uri(reverse("registrations:index"))) + 'email_confirm/' + \
		generate_email_token(Participant.objects.get(email=send_to)) + '/'
		print('Email url \t',verify_email_url)
		mail.body = mail.body%(name.title(), verify_email_url)
		content = Content('text/html', mail.body)
		# 
		# print(data['events'][0])
		try:
			mail_1 = Mail(mail.from_email, mail.subject, to_email, content)
			response = send_grid.sg.client.mail.send.post(request_body = mail_1.get())
			if response.status_code%100!=2:
				raise Exception
			print(response)
		except Exception as e:
		    print("\t",e)
		    participant.delete()
		    return JsonResponse({'status':0, 'message':'Error sending email. Please try again.'})

		message ="A confirmation link has been sent to {email}. Kindly click on it to verify your email address.".format(email=send_to)
		# message='hello'
		return JsonResponse({'status':1,'message':message})