from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from oasis2018.settings_config import keyconfig
from registrations.views import send_grid
from events.models import MainParticipation, MainEvent
from registrations.models import Participant,College, PaymentGroup

import requests
import json
import re
import sendgrid
import string

from sendgrid.helpers.mail import *
from utils.registrations import *
from instamojo_wrapper import Instamojo

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits


api = Instamojo(api_key=keyconfig.INSTA_API_KEY_test, auth_token=keyconfig.AUTH_TOKEN_test, endpoint='https://test.instamojo.com/api/1.1/') #when in development




@csrf_exempt
def index(request):
    '''
    To register a new participant and send him a verification link
    Or, if the participant is logged in, his index page.
    '''

    if request.method=='POST':
        print("post request")
        print("******** POST ***********")
        data = json.loads(request.body.decode('utf8').replace("'", '"'))
        print(request.body)
        print (data)
        recaptcha_response = data['reCaptcha']
        data_1={
            'secret' : keyconfig.google_recaptcha_secret_key,
            'response' : recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data_1)
        
        result=r.json()
        if not result['success']:
            print(result)
            return JsonResponse({'status':0, 'message':'Invalid Recaptcha. Try Again'})
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
        if len(data.get('events')) == 0:
            return JsonResponse({'status':0,'message':'Please select at least one event'})
        else:
            try:
                participant = Participant()
                participant.name = str(data['name'])
                participant.gender = str(data['gender'])
                participant.city = str(data['city'])
                participant.email = str(data['email'])
                try:
                    participant.college = College.objects.get(name = data['college'])
                except:
                    return JsonResponse({'status':0,'message':'Invalid College'})
                participant.phone = int(data['phone'])
                if data['head_of_society']:
                    participant.head_of_society = True
                else:
                    participant.head_of_society = False
                try:
                    year = int(data['year_of_study'])
                    if year not in range(6):
                        return JsonResponse({'message':'Invalid year', 'status':0})
                    participant.year_of_study = year
                except:
                     return JsonResponse({'status':0,'message':'Invalid year of study'})

            except KeyError as missing_data:
                response = JsonResponse({'message':'Data is Missing: {}'.format(missing_data), 'x_status': 4})
                # response.delete_cookie('sessionid')
                return response
            participant.save()

            
            for key in data.get("events"):
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
    
    if request.user.is_authenticated():
        user = request.user
        print(user)
        try:
            participant = Participant.objects.get(user=user)
        except:
            pass
        participation_set = MainParticipation.objects.filter(participant=participant)
        cr = Participant.objects.get(college=participant.college, is_cr=True)
        return render(request,'registrations/home.html',{'participant':participant,\
        'participations':participation_set,'cr':cr})


    print("get request")
    print("****** PRINTING *******")
#   print("just printed :)")
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

        # return HttpResponse('Redirect')

@csrf_exempt
def home(request):
    '''
    Login page
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        
        if user is not None:
            if user.is_active:
                try:
                    if not user.participant.email_verified:
                        message = "It seems you haven\'t verified your email yet. Please verify it as soon as possible to proceed.For any query, call the following members of the Department of Publications and Correspondence. Aditi Pandey: %s - pcr@bits-oasis.org ."%(get_pcr_number())
                        context = {'error_heading':'Email not verified','message' : message,'url':request.build_absolute_uri(reverse('registrations:home'))}
                        return render(request, 'registrations/message.html', context)

                    login(request,user)
                    return redirect('registrations:index')

                except:
                    message = "Participant does not Exist"
                    context = {'error_heading':'No Participant','message' : message,'url':request.build_absolute_uri(reverse('registrations:home'))}
                    return render(request, 'registrations/message.html', context)

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

def forgot_password(request):
    if(request.method=='POST'):
        data = request.POST
        print(data)
        email = data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return JsonResponse({'status':0, 'message':'Please enter a valid email address.'})
        try:
            participant = Participant.objects.get(email=email)
            user=participant.user
            username = user.username
            password = ''.join(choice(chars) for i in range(8))
            user.set_password(password)
            user.save()

            email_class = send_grid.ForgotPassword()
            name = participant.name
            send_to = participant.email
            login_url = str(request.build_absolute_uri(reverse('registrations:home')))
            body = email_class.body%(name,login_url,username,password,get_pcr_number())
            to_email=Email(send_to)
            content = Content('text/html', body)
            try:
                mail = Mail(email_class.from_email,email_class.subject,to_email,content)
                response = send_grid.sg.client.mail.send.post(request_body = mail.get())
                print("EMAIL SENT")
            except:
                context = {
                    'status': 0,
                    'error_heading': "Error sending mail",
                    'message': "Sorry! Error in sending email. Please try again.",
                }
                return render(request, 'registrations/message.html', context)

            context = {
            'error_heading':"Emails sent",
            'message' : "Login credentials have been mailed to the corresponding participant."
            }
            return render(request, 'registrations/message.html', context)

        except Exception as e:
            print(e)
            context = {
                    'error_heading': "Invalid Email",
                    'message': "Sorry, your email is not registered. Please register again.",
                    'url':request.build_absolute_uri(reverse('registrations:home'))
                    }
            return render(request, 'registrations/message.html', context)
    else:
        return render(request,'registrations/forgot_password.html')


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

@login_required
@csrf_exempt
def payment(request):
    participant = Participant.objects.get(user=request.user)
    # print(participant)
    if not participant.pcr_approved:
        context = {
        'error_heading': "Invalid Access",
        'message': "You are yet not approved by Department of PCr, Bits Pilani.",
        'url':request.build_absolute_uri(reverse('registrations:index'))
        }
        return render(request, 'registrations/message.html', context)
    if request.method=='GET':
        return render(request, 'registrations/participant_payment.html', {'participant':participant})
    if request.method == 'POST':
        print("***********")
        try:
            key = request.POST['key']
            # print(key)
        except:
            return redirect('registrations:payment')
        if int(request.POST['key']) == 1:
            amount = 300
            programId = 9381
        elif int(request.POST['key']) == 2:
            amount = 1000
            programId = 9183
        elif int(request.POST['key']) == 3:
            amount = 700
            programId = 9382
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        name = participant.name
        email = participant.email
        phone = participant.phone
        college = participant.college
        gender = participant.gender
        purpose = 'Payment for OASIS \'18'

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
            "totalFare":amount,
            "addExtra":0,
            "attendingEvents":[
                {
                    "programId":programId,
                    "programName":"Oasis 2018 Registrations",
                    "subProgramName":"Registration",
                    "fare":amount,
                    "attendees":[
                        {
                            "name":name,
                            "email":email,
                            "phone":phone,
                            "college":college.name,
                            # "sex":gender,
                            "extraInfoValue":"BENGALURU"
                        }
                    ]
                }
            ]
        }
        book_url = 'https://www.thecollegefever.com/v1/booking/bookticket'
        cookies = {'auth':session}
        book_response = requests.post(url=book_url, headers=headers, data=json.dumps(book_data), cookies=cookies)
        status_code_2 = book_response.status_code
        # if status_code_2==200:
        json_ob_2 = json.loads(book_response.text)
        print(json_ob_2)
        
        page = json_ob_2['pgUrl']
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

def payment_response(request):
    import requests
    payid=str(request.GET['payment_request_id'])
    try:
        headers = {'X-Api-Key': keyconfig.INSTA_API_KEY, 'X-Auth-Token': keyconfig.AUTH_TOKEN}
        r = requests.get('https://www.instamojo.com/api/1.1/payment-requests/'+str(payid),headers=headers)
    except:
        headers = {'X-Api-Key': keyconfig.INSTA_API_KEY_test, 'X-Auth-Token': keyconfig.AUTH_TOKEN_test}
        r = requests.get('https://test.instamojo.com/api/1.1/payment-requests/'+str(payid), headers=headers)
    json_ob = r.json()
    print(json_ob)
    if (json_ob['success']):
        payment_request = json_ob['payment_request']
        purpose = payment_request['purpose']
        amount = payment_request['amount']
        amount = int(float(amount))
        try:
            group_id = int(purpose.split(' ')[1])
            payment_group = PaymentGroup.objects.get(id=group_id)
            count = payment_group.participant_set.all().count()
            print("COUNT=",count)
            print("A/C=",amount/count)
            print(payment_group.participant_set.all())
            if (amount/count) == 1000:
                for part in payment_group.participant_set.all():
                    part.controlz_paid = True
                    part.paid = True
                    part.save()
            elif (amount/count) == 700:
                for part in payment_group.participant_set.all():
                    if part.paid:
                        part.controlz_paid = True
                        part.save()

            elif (amount/count) == 300:
                for part in payment_group.participant_set.all():
                    print(part.name,end="\n\n")
                    part.paid = True
                    part.save()

        except Exception as e:     
            print(e)
            email = payment_request['email']
            participant = Participant.objects.get(email=email)
            if amount == 1000:
                participant.controlz_paid = True
            elif amount == 650.00 and participant.paid:
                participant.controlz_paid = True
            participant.paid = True
            participant.save()
        context = {
            'error_heading' : "Payment successful",
            'message':'Thank you for paying.',
            'url':request.build_absolute_uri(reverse('registrations:index'))
            }
        return render(request, 'registrations/message.html', context)
    
    else:
        context = {
            'error_heading': "Payment error",
            'message': "An error was encountered while processing the payment. Please contact PCr, BITS, Pilani.",
            'url':request.build_absolute_uri(reverse('registrations:index'))
            }
        return render(request, 'registrations/message.html', context)       
