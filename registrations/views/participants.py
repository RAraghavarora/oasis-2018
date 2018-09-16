from events.models import MainParticipation, MainEvent
from registrations.models import Participant,College
from django.shortcuts import render,redirect
import requests
from oasis2018 import keyconfig
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
import re
from registrations.views import send_grid
import sendgrid
from sendgrid.helpers.mail import *
from utils.registrations import *
from django.contrib import messages
from instamojo_wrapper import Instamojo
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    '''
    To register a new participant and send him a verification link
    '''
    if request.user.is_authenticated():
        user = request.user
        print(user)
        participant = Participant.objects.get(user=user)
        participation_set = MainParticipation.objects.filter(participant=participant)
        cr = Participant.objects.get(college=participant.college, is_cr=True)
        return render(request,'registrations/home.html',{'participant':participant,\
        'participations':participation_set,'cr':cr})
    
    if request.method=='GET':
        print("get request")
        print("****** PRINTING *******")
#	print("just printed :)")
        colleges = College.objects.all()
        c_names = [college.name for college in colleges]
        events = [{'name':event.name,'id':event.id} for event in MainEvent.objects.all() ]
	# e_names = [event.name for event in events]
        # data = serializers.serialize('json', c_names)
        # data1 = serializers.serialize('json', e_names)
        data={'colleges':c_names,'events':events}
        return HttpResponse(json.dumps(data))
        # return HttpResponse(x, content_type="application/json")
        # return render(request, 'registrations/signup.html', {'college_list':colleges, 'event_list':events})
    
    if request.method=='POST':
        print("post request")
        print("******** POST ***********")
        data = request.POST
        # print(request.body)
        # print(type(request.body))
        #data = request.body.decode('utf8').replace("'", '"')
        print (data)
        # data = json.loads(data['POST'])
        #data = json.loads(data)
        # print(type(data.get('events[]')))
        # recaptcha_response = data['g-recaptcha-response']
        # data_1={
        #     'secret' : keyconfig.google_recaptcha_secret_key,
        #     'response' : recaptcha_response
        # }
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data_1)
        
        # result=r.json()
        # if not result['success']:
        #     print(result)
        #     return JsonResponse({'status':0, 'message':'Invalid Recaptcha. Try Again'})
        if len(data['phone'])!=10:
            return JsonResponse({'status':0,'message':'Please enter a valid contact number.'})

        email = data['email']
        print (email)
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            print("1")
            return JsonResponse({'status':0, 'message':'Please enter a valid email address.'})
        
        try:
            Participant.objects.get(email=email)
            print("try")
            return JsonResponse({'status':0, 'message':'Email already registered.'})
        except:
            print("except")
            pass
        print("THIS:\t",data.getlist("events[]"))
        if len(data.getlist('events')) == 0:
            print("YES")
            return JsonResponse({'status':0,'message':'Please select at least one event'})
        else:
            print("IN ELSE\n")
            participant = Participant()
            participant.name = str(data['name'])
            participant.gender = str(data['gender'])
            participant.city = str(data['city'])
            participant.email = str(data['email'])
            participant.college = College.objects.get(name = data['college'])
            print(data['college'])
            print(type(data['college']))
            print(type(str(data['college'])))
            participant.phone = int(data['phone'])
            if str(data['head_of_society']) == 'True':
                participant.head_of_society = True
            else:
                participant.head_of_society = False
            participant.year_of_study = int(data['year_of_study'])
            participant.save()

            
            for key in data.getlist("events[]"):
                event = MainEvent.objects.get(name=str(key))
                MainParticipation.objects.create(event = event, participant = participant)
            participant.save()
            mail = send_grid.register()
            send_to = str(data["email"])
            name = str(data['name'])
            to_email = Email(send_to)
            verify_email_url = str(request.build_absolute_uri(reverse("registrations:index"))) + 'email_confirm/' + \
            generate_email_token(Participant.objects.get(email=send_to)) + '/'
            print('Email url \t',verify_email_url)
            mail.body = mail.body%(name.title(), verify_email_url)
            content = Content('text/html', mail.body)
            # 
            print(data['events'][0])
            try:
                mail_1 = Mail(mail.from_email, mail.subject, to_email, content)
                response = send_grid.sg.client.mail.send.post(request_body = mail_1.get())
                print(response)
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
        # print(request.POST)
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

@login_required
def manage_events(request):
    participant = Participant.objects.get(user=request.user)
    if request.method == 'POST':
        data = request.POST
        if data['action'] == 'add':
            try:
                events_id = data.getlist('events_id')
            except:
                return redirect(request.META.get('HTTP_REFERER'))
            for event_id in events_id:
                event = MainEvent.objects.get(id=event_id)
                p, created  = MainParticipation.objects.get_or_create(participant=participant, event=event)

        if data['action'] == 'remove':
            not_removed = []
            try:
                events_id = data.getlist('events_id')
            except:
                return redirect(request.META.get('HTTP_REFERER'))
            print(events_id)
            for event_id in events_id:
                try:
                    event = MainEvent.objects.get(id=event_id)
                    participation = MainParticipation.objects.get(participant=participant, event=event)
                    if not participation.pcr_approved:
                        participation.delete()
                    else:
                        not_removed.append(participation)
                except Exception as e:
                    print(e)
                    pass
                print(not_removed)
            if len(not_removed) != 0:
                return render(request, 'remove.html', {'events':not_removed})
    added_list = [participation for participation in MainParticipation.objects.filter(participant=participant)]
    added_events = [p.event for p in added_list]
    not_added_list = [event for event in MainEvent.objects.all() if event not in added_events]
    return render(request, 'registrations/manage_events.html', {'added_list':added_list, 'not_added_list':not_added_list, 'participant':participant})

@login_required
def get_profile_card(request):
    participant = Participant.objects.get(user=request.user)
    if not participant.firewallz_passed:
        if not participant.is_guest:
            context = {
                    'error_heading': "Invalid Access",
                    'message': "Please pass firewallz booth at BITS to access this page.",
                    'url':request.build_absolute_uri(reverse('registrations:index'))
                    }
            return render(request, 'registrations/message.html', context)
    participant = Participant.objects.get(user=request.user)
    participation_set = MainParticipation.objects.filter(participant=participant, pcr_approved=True)
    events = ''
    for participation in participation_set:
        events += participation.event.name + ', '
    events = events[:-2]
    return render(request, 'registrations/profile_card.html', {'participant':participant, 'events':events,})

def return_qr(request):
    text = request.GET.get('text')
    qr = generate_qr_code(text)
    response = HttpResponse(content_type="image/jpeg")
    qr.save(response, "JPEG")
    return response


# @login_required
# def upload_docs(request):
# 	participant = Participant.objects.get(user=request.user)
# 	if request.method == 'POST':
# 		from django.core.files import File
# 		if participant.pcr_approved:
# 			context = {
# 					'error_heading': "Permission Denied",
# 					'message': "You have already been approved by PCr, BITS Pilani as a partcipant. Contact pcr@bits-oasis.org to change your uploads.",
# 					'url':request.build_absolute_uri(reverse('registrations:index'))
# 					}
# 			return render(request, 'registrations/message.html', context)
# 		try:
# 			image = request.FILES['profile_pic']
# 			image = participant.profile_pic
# 			if image is not None:
# 				image.delete(save=True)
# 			up_img = request.FILES['profile_pic']
# 			img_file = resize_uploaded_image(up_img, 240, 240)
# 			new_img = File(img_file)
# 			participant.pcr_approved = False
# 			participant.profile_pic.save('profile_pic', new_img)
# 		except:
# 		 	pass
# 		try:
# 			verify_docs = request.FILES['verify_docs']
# 			docs = participant.verify_docs
# 			if docs is not None:
# 				docs.delete(save=True)
# 			up_docs = request.FILES['verify_docs']
# 			doc_file = resize_uploaded_image(up_docs, 400, 400)
# 			new_docs = File(doc_file)
# 			participant.pcr_approved = False
# 			participant.verify_docs.save('verify_docs', new_docs)
# 		except:
# 			pass
# 	try:
# 		image_url = request.build_absolute_uri('/')[:-1] + participant.profile_pic.url
# 		image = True
# 	except:
# 		image_url = '#'
# 		image = False
# 		pass
# 	try:
# 		docs_url = request.build_absolute_uri('/')[:-1] + participant.verify_docs.url
# 		docs = True
# 	except:
# 		docs_url = '#'
# 		docs = False
# 		pass
# 	return render(request, 'registrations/upload_docs.html', {'participant':participant, 'image_url':image_url, 'image':image, 'docs_url':docs_url, 'docs':docs})

# @login_required
# def payment(request):
#     participant = Participant.objects.get(user=request.user)
#     # print(participant)
#     if not participant.pcr_approved:
#         context = {
#         'error_heading': "Invalid Access",
#         'message': "You are yet not approved by Department of PCr, Bits Pilani.",
#         'url':request.build_absolute_uri(reverse('registrations:index'))
#         }
#         return render(request, 'registrations/message.html', context)
#     if request.method=='GET':
#         return render(request, 'registrations/participant_payment.html', {'participant':participant})
#     if request.method == 'POST':
#         print("***********")
#         try:
#             key = request.POST['key']
#             # print(key)
#         except:
#             return redirect(request.META.get('HTTP_REFERER'))
#         if int(request.POST['key']) == 1:
#             amount = 300
#         elif int(request.POST['key']) == 2:
#             amount = 950
#         elif int(request.POST['key']) == 3:
#             amount = 650
#         else:
#             return redirect(request.META.get('HTTP_REFERER'))
#         name = participant.name
#         email = participant.email
#         phone = participant.phone
#         purpose = 'Payment for OASIS \'18'
#         response = api.payment_request_create(
#             amount = amount,
#             purpose = purpose,
#             # send_email = False,
#             buyer_name = name,
#             email = email,
#             phone = phone,
#             redirect_url = request.build_absolute_uri(reverse("registrations:hello"))
#         )
#         print(response)
#         # print(response['payment_request']['status'])
#         # print(email)
#         # print(response['payment_request']['longurl'])
        
#         try:
#             url = response['payment_request']['longurl']
#             return HttpResponseRedirect(url)
#         except Exception as e:
#             print(e)
#             context = {
#             'error_heading': "Payment error",
#             'message': "An error was encountered while processing the request. Please contact PCr, BITS, Pilani.",
#             'url':request.build_absolute_uri(reverse('registrations:make_payment'))
#             }
#             return render(request, 'registrations/message.html')


# def payment_response(request):
#     import requests
#     payid=str(request.GET['payment_request_id'])
#     print(keyconfig.INSTA_API_KEY_test)
#     headers = {'X-Api-Key': keyconfig.INSTA_API_KEY_test,
#     'X-Auth-Token': keyconfig.AUTH_TOKEN_test}
#     print(headers)
#     try:
#         r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
#     except:
#         r = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)    ### when in development
#     json_ob = r.json()
#     print(json_ob)
#     if (json_ob['success']):
#         payment_request = json_ob['payment_request']
#         purpose = payment_request['purpose']
#         print("purpose\t",purpose)
#         amount = payment_request['amount']
#         amount = int(float(amount)) 
#         try:
#             group_id = int(purpose.split(' ')[1])
#             print('group id\t',group_id)
#             return HttpResponse('ajsp')
#         except Exception as e:
#             return HttpResponse(e)
#         # payment_group = PaymentGroup.objects.get(id=group_id)
#         # count = payment_group.participant_set.all().count()
#         # if (amount/count) == 950:
#         # for part in payment_group.participant_set.all():
#         # part.controlz_paid = True
#         # part.paid = True
#         # part.save()
#         # elif (amount/count) == 650:
#         # for part in payment_group.participant_set.all():
#         # if part.paid:
#         # part.controlz_paid = True
#         # part.save()

#         # elif (amount/count) == 300:
#         # for part in payment_group.participant_set.all():
#         # part.paid = True
#         # part.save()

#         # except:
#         # email = payment_request['email']
#         # print amount
#         # print type(amount)
#         # participant = Participant.objects.get(email=email)
#         # if amount == 950:
#         # participant.controlz_paid = True
#         # elif amount == 650.00 and participant.paid:
#         # participant.controlz_paid = True
#         # participant.paid = True
#         # participant.save()
#         # context = {
#         # 'error_heading' : "Payment successful",
#         # 'message':'Thank you for paying.',
#         # 'url':request.build_absolute_uri(reverse('registrations:index'))
#         # }
#         # return render(request, 'registrations/message.html', context)

#         # else:

#         # payment_request = json_ob['payment_request']
#         # purpose = payment_request['purpose']
#         # email = payment_request['email']
#         context = {
#         'error_heading': "Payment error",
#         'message': "An error was encountered while processing the payment. Please contact PCr, BITS, Pilani.",
#         'url':request.build_absolute_uri(reverse('registrations:index'))
#         }
#         return render(request, 'registrations/message.html', context)
#     return HttpResponse('testing da')
