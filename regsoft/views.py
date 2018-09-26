from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from registrations.models import *
from .models import *
from events.models import *
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from functools import reduce
from registrations.urls import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from oasis2018.settings import BASE_DIR
import os
from time import gmtime, strftime
import string
# from pcradmin.views import get_cr_name, gen_barcode, get_pcr_number
from django.contrib import messages
from django.contrib.auth.models import User

import sendgrid
from sendgrid.helpers.mail import *
from . import send_grid

import os
import re

from utils.registrations import get_pcr_number

from oasis2018.settings_config.keyconfig import *
from random import sample, choice
from django.contrib import messages
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

###Helper function to get the group leader##
def get_group_leader(group):
    return group.participant_set.get(is_g_leader=True)

#To create a code for the group
def generate_group_code(group):
    group_id = group.id
    encoded = group.group_code
    if encoded == '':
        raise ValueError
    if encoded is not None:
        return encoded
    group_ida = "%04d" % int(group_id)
    college_code = ''.join(get_group_leader(group).college.name.split(' '))
    if len(college_code)<4:
        college_code += str(0)*(4-len(college_code))
    group.group_code = college_code + group_ida
    group.save()
    return encoded

############FIREWALLS#############

@staff_member_required
def firewallz_home(request):
    college_list = [college for college in College.objects.all() if college.participant_set.filter(is_cr=True)]

    rows = []
    for college in college_list:
        name = college.name
        cr = college.participant_set.get(college=college, is_cr=True).name
        total_final = college.participant_set.filter(pcr_final=True).count()
        firewallz_passed = college.participant_set.filter(pcr_final=True, firewallz_passed=True).count()
        url = request.build_absolute_uri(reverse('regsoft:firewallz_approval', kwargs={'c_id':college.id}))
        rows.append({'data': [name,cr,total_final,firewallz_passed] , 'link':[{'url':url,'title':'Approve Participants'},]})

    print(rows)
    headings = ['College', 'CR', 'PCr Finalised Participants', 'Firewallz Passed','Approve Participants']
    title = 'Select college to approve Participants'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title
    }
    print(table)
    return render(request, 'regsoft/tables.html', {'tables':[table,]})

@staff_member_required
def firewallz_approval(request, c_id):
    college = get_object_or_404(College, id=c_id)
    if request.method == 'POST':
        try:
            data = request.POST
            id_list = data.getlist('id_list')
        except:
            return redirect(request.META.get('HTTP_REFERER'))
        try:
            g_leader_id = data['g_leader_id']
            if not g_leader_id in id_list:
                messages.warning(request,'Please select a Group Leader from the participant list.')
                return redirect(request.META.get('HTTP_REFERER'))   
            g_leader = Participant.objects.get(id=g_leader_id)
            g_leader.is_g_leader = True
            g_leader.save()
        
        except:
            messages.warning(request,'Please select a Group Leader.')
            return redirect(request.META.get('HTTP_REFERER'))
        
        group = Group.objects.create()
        for part_id in id_list:
            part = Participant.objects.get(id=part_id)
            if part.group is not None:
                g_leader.is_g_leader = False
                g_leader.save()
                group.delete()
                context = {
                    'error_heading': "Error",
                    'message': "Participant(s) already in a group",
                    'url':request.build_absolute_uri(reverse('regsoft:firewallz_home'))
                    }
                return render(request, 'registrations/message.html', context)
            part.firewallz_passed=True
            part.group = group
            part.save() 
        encoded = generate_group_code(group)
        group.save()
        part_list = Participant.objects.filter(id__in=id_list)
        return redirect(reverse('regsoft:get_group_list', kwargs={'g_id':group.id}))
    groups_passed = [group for group in Group.objects.all() if get_group_leader(group).college == college]
    unapproved_list = college.participant_set.filter(pcr_final=True, firewallz_passed=False, is_guest=False)
    print (groups_passed)
    return render(request, 'regsoft/firewallz_approval.html', {'groups_passed':groups_passed, 'unapproved_list':unapproved_list, 'college':college})


@staff_member_required
def get_group_list(request, g_id):
    group = get_object_or_404(Group, id=g_id)
    if request.method == 'POST':
        try:
            data = request.POST
            id_list = data.getlist('id_list')
        except:
            return redirect(request.META.get('HTTP_REFERER'))

        participant_list = Participant.objects.filter(id__in=id_list)
        for participant in participant_list:
            if participant.is_g_leader:
                messages.warning(request,'Cannot unconfirm a Group Leader.')
                continue
            participant.group = None
            participant.firewallz_passed = False
            participant.save()
        leader = get_group_leader(group)
        if group.participant_set.count == 0:
            group.delete()
        return redirect(reverse('regsoft:firewallz_approval', kwargs={'c_id':leader.college.id}))
    participant_list = group.participant_set.all()
    return render(request, 'regsoft/group_list.html', {'participant_list':participant_list, 'group':group})

@staff_member_required
def add_guest(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        email = data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            messages.warning(request,'Please enter a valid email address.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                Participant.objects.get(email=data['email'])
                messages.warning(request,'Email already registered.')
                return redirect(request.META.get('HTTP_REFERER'))
            except:
                pass
            participant = Participant()
            participant.name = str(data['name'])
            participant.gender = str(data['gender'])
            participant.city = str(data['city'])
            participant.email = str(data['email'])
            participant.college = College.objects.get(name=str(data['college']))
            participant.phone = int(data['phone'])
            participant.is_guest = True
            participant.email_verified = True
            try:
                participant.bits_id = str(data['bits_id'])
            except:
                messages.warning(request, 'Please enter the bits id')
                return redirect(request.META.get('HTTP_REFERER'))
            participant.save()
            participant.firewallz_passed = True
            
            # ems_code = str(participant.college.id).rjust(3,'0') + str(participant.id).rjust(4,'0')
            # participant.ems_code = ems_code
            # participant.save()ss
            username = participant.name.split(' ')[0] + str(participant.id)
            print(participant.id)
            password = ''.join(choice(chars) for i in range(8)) #random alphanumeric password of length 8
            user = User.objects.create_user(username=username, password=password)
            participant.user = user
            participant.save() # Barcode will automatically be generated and assigned

            email_class = send_grid.add_guest()

            send_to = participant.email
            name = participant.name
            body = email_class.body%(name, username, password, get_pcr_number())
            to_email = Email(send_to)
            content = Content('text/html', body)

            try:
                mail = Mail(email_class.from_email,email_class.subject,to_email,content)
                response = send_grid.sg.client.mail.send.post(request_body = mail.get())
                print("EMAIL SENT")
            except:
                participant.user = None
                participant.save()
                user.delete()
                participant.delete()
                context = {
                    'url':request.build_absolute_uri(reverse('regsoft:firewallz_home')),
                    'error_heading': "Error sending mail",
                    'message': "Sorry! Error in sending email. Please try again.",
                }
                return render(request, 'registrations/message.html', context)

            context = {
                'error_heading': "Emails sent",
                'message': "Login credentials have been mailed to the corresponding new participants.",
                'url':request.build_absolute_uri(reverse('regsoft:firewallz_home'))
            }
            return render(request, 'registrations/message.html', context)
    else:
        colleges = College.objects.all()
        guests = Participant.objects.filter(is_guest=True)
        return render(request, 'regsoft/add_guest.html', {'colleges':colleges, 'guests':guests})

@staff_member_required
def remove_guests(request):
    if request.method == 'POST':
        data = request.POST
        try:
            list = data.getlist('guest_list')
        except:
            messages.warning(request, 'No guest selected.')
            return redirect(request.META.get('HTTP_REFERER'))
        participants=Participant.objects.filter(id__in=data.getlist('guest_list'), is_guest=True)
        for participant in participants:
            user = participant.user
            participant.user = None
            user.delete()
        participants.delete()
    return redirect(reverse('regsoft:add_guest'))
    

# #########Recnacc#########

@staff_member_required
def recnacc_home(request):
    rows=[{'data':[group.group_code,get_group_leader(group).name,get_group_leader(group).college.name,get_group_leader(group).phone,group.created_time,group.participant_set.filter(controlz=True).count(),group.participant_set.filter(checkout_group__isnull=False).count()], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:allocate_participants', kwargs={'g_id':group.id})), 'title':'Allocate Participants'}]} for group in Group.objects.all().order_by('-created time')]
    title='Groups that have passed Firewallz'
    headings = ['Group Code', 'Group Leader', 'College', 'Gleader phone', 'Firewallz passed time', 'Total controls passed','Total alloted', 'Checkout','View Participants']

    table={
        'rows':rows,
        'title':title,
        'headings':headings
    }
    return render(request,'regsoft/tables.html',{'tables':[table,]})


@staff_member_required
def allocate_participants(request,g_id):
    group=get_object_or_404(Group,id=g_id)
    if request.method=='POST':
        from datetime import datetime
        data=request.POST
        try:
            group.amount_deduct=data['amount_retained']
            group.save()
        except:
            pass
        if data['action']=='allocate':
            try:
                parts_id=data.getlist('data')
                room_id=data['room']
                room=Room.objects.get(id=room_id)
            except:
                messages.warning(request,'Incomplete selection')
                return redirect(request.META.get('HTTP_REFERER'))
            if not parts_id:
                messages.warning(request,'Incomplete selection')
                return redirect(request.META.get('HTTP_REFERER'))
            rows=[]
            room.vacancy-=len(parts_id)
            room.save()
            for part_id in parts_id:
                part=Participant.objects.get(id=part_id)
                part.acco=True
                part.room=room
                part.recnacc_time=datetime.now()
                part.save()
        elif data['action']=='deallocate':
            try:
                parts_id = data.getlist('data')
            except:
                return redirect(request.META.get('HTTP_REFERER'))
            for part_id in parts_id:
                part = Participant.objects.get(id=part_id)
                room = part.room
                room.vacancy += 1
                room.save()
                part.acco = False
                part.room = None
                part.save()
        return redirect(reverse('regsoft:recnacc_group_list',kwargs={'c_id':get_group_leader(group).college.id}))
    else:
        room_list=Room.objects.all()
        unalloted_participants=group.participant_set.filter(acco=False,checkout_group=None,controlz=True)
        alloted_participants=group.participant_set.filter(acco=True,checkout_group=None,controlz=True)
        checked_out=group.participant_set.filter(checkout_group__isnull=False)
        return render(request,'regsoft/allot.html',{'unalloted':unalloted_participants,'alloted':alloted_participants,'rooms':room_list,'group':group,'checked_out':checked_out
    })


@staff_member_required
def recnacc_group_list(request,c_id):
    college=get_object_or_404(College,id=c_id)
    group_list=[group for group in Group.objects.all() if get_group_leader(group).college==college]
    complete_groups = [group for group in group_list if all(part.acco for part in group.participant_set.filter(controlz=True))]
    incomplete_groups=[group for group in group_list if not group in complete_groups]

    complete_rows = [{'data':[group.created_time, get_group_leader(group).name, group.participant_set.filter(controlz=True).count(), group.participant_set.filter(acco=True,checkout_group=None, controlz=True).count()], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:allocate_participants', kwargs={'g_id':group.id})), 'title':'Manage group'}]} for group in complete_groups]

    incomplete_rows = [{'data':[group.created_time, get_group_leader(group).name, group.participant_set.filter(controlz=True).count(), group.participant_set.filter(acco=True,checkout_group=None, controlz=True).count()], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:allocate_participants', kwargs={'g_id':group.id})), 'title':'Manage group'}]} for group in incomplete_groups]

    complete_table={
        'rows':complete_rows,
        'headings':['Created Time','GroupLeader Name','Total','Alloted','Manage'],
        'title':'Completely alloted groups from'+college.name
    }
    incomplete_table={
        'rows':incomplete_rows,
        'headings':['Created Time','GroupLeader Name','Total','Alloted','Manage'],
        'title':'Incompletely alloted groups from'+college.name
    }
    return render(request,'regsoft/tables.html',{'tables':[complete_table,incomplete_table],'college':college})


@staff_member_required
def room_details(request):
    room_list=Room.objects.all()
    rows = [{'data':[room.room, room.bhavan.name, room.vacancy, room.capacity,], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:manage_vacancies', kwargs={'r_id':room.id})), 'title':'Manage'},]} for room in room_list]
    headings=['Room','Bhawan','Vacancy','Capacity']
    title = 'Manage Room Details'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title,
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,]})


@staff_member_required
def manage_vacancies(request,r_id):
    room=get_object_or_404(Room,id=r_id)
    if request.method=='POST':
        data=request.POST
        try:
            note=data['note']
        except:
            messages.warning(request,'Please add a note.')
        try:
            room.vacancy=data['vacancy']
            room.save()
        except:
            pass
        try:
            capacity=room.capacity
            vacancy=int(data['capacity'])-capacity
            room.vacancy=int(data['vacancy'])+vacancy
            room.capacity=data['capacity']
            room.save()
        except:
            pass

        re_note=Note()
        re_note.note=note
        re_note.room=room
        re_note.save()
        return redirect(reverse('regsoft:room_details'))
    else:
        notes=room.note_set.all()
        return render(request,'regsoft/manage_vacancies.html',{'room':room,'notes':notes})

@staff_member_required
def recnacc_bhavans(request):
    rows =[{'data':[bhavan.name, reduce(lambda x,y:x+y.vacancy, bhavan.room_set.all(), 0),], 'link':[{'title':'Details', 'url':request.build_absolute_uri(reverse('regsoft:bhavan_details', kwargs={'b_id':bhavan.id}))},] } for bhavan in Bhavan.objects.all()]
    headings = ['Bhavan', 'Vacancy', 'Room-wise details']
    tables = [{'title':'All Bhavans', 'headings':headings, 'rows':rows}]
    return render(request,'regsoft/tables.html', {'tables':tables})

@staff_member_required
def bhavan_details(request, b_id):
    bhavan = Bhavan.objects.get(id=b_id)
    rows = [{'data':[room.room, room.vacancy, room.capacity], 'link':[{'title':'Details', 'url':request.build_absolute_uri(reverse('regsoft:manage_vacancies', kwargs={'r_id':room.id}))},]} for room in bhavan.room_set.all()]
    headings = ['Room', 'Vacancy', 'Capacity', 'Manage Vacancies']
    tables = [{'title': 'Details for ' + bhavan.name + ' bhavan', 'headings':headings, 'rows':rows}]
    return render(request, 'regsoft/tables.html', {'tables':tables})

@staff_member_required
def group_vs_bhavan(request):
    rows=[]
    for group in Group.objects.all():
        if group.participant_set.filter(acco=True):
            bhavans=[]
            for part in group.participant_set.filter(acco=True):
                if not part.room.bhavan in bhavans:
                    bhavans.append(part.room.bhavan)
            for bhavan in bhavans:
                rows.append({'data':[bhavan.name,get_group_leader(group).college.name,group.group_code, get_group_leader(group).name, group.participant_set.filter(acco=True, room__bhavan=bhavan).count(), get_group_leader(group).phone],'link':[]})
    table = {
        'rows':rows,
        'headings':['Bhavan','College','Group Code', 'Group Leader', 'Number of participants in bhavan', 'Group Leader Phone'],
        'title':'Group vs Bhavans'
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,]})


@staff_member_required
def college_details(request):
    college_list=[]
    for college in College.objects.all():
        try:
            part=college.participant_set.filter(is_cr=True)
            college_list.append(college)
        except:
            pass

    rows = [{'data':[college.name, college.participant_set.get(is_cr=True).name,college.participant_set.filter(acco=True).count()], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:recnacc_group_list', kwargs={'c_id':college.id})), 'title':'View Details'}]} for college in college_list]
    headings = ['College', 'Cr Name','Alloted Participants', 'View Details']
    title = 'Select college to approve Participants'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,]})

@staff_member_required
def checkout_college(request):
    rows = [{'data':[college.name,college.participant_set.filter(acco=True).count(), college.participant_set.filter(checkout_group__isnull=False).count()],'link':[{'title':'Checkout', 'url':request.build_absolute_uri(reverse('regsoft:checkout', kwargs={'c_id':college.id}))}] } for college in College.objects.all()]
    tables = [{'title':'List of Colleges', 'rows':rows, 'headings':['College', 'Alloted Participants', 'Checked out Participants','Checkout']}]
    return render(request, 'regsoft/tables.html', {'tables':tables})

###Helper function to generate checkout group code###
def generate_ckgroup_code(group):
    group_id=group.id
    encoded=group.group_code
    if encoded=='':
        raise ValueError
    if encoded is not None:
        return encoded
    group_ida = "%04d" % int(group_id)
    college_code = ''.join(group.participant_set.all()[0].college.name.split(' '))
    if len(college_code)<4:
        college_code += str(0)*(4-len(college_code))
    group.group_code = college_code + group_ida
    group.save()
    return encoded

@staff_member_required
def checkout(request,c_id):
    college=get_object_or_404(College,id=c_id)
    if request.method=='POST':
        data=request.POST
        try:
            part_list=Participant.objects.filter(id__in=data.getlist('part_list'))
        except:
            return redirect(request.META.get('HTTP_REFERER'))
        checkout_group=CheckoutGroup.objects.create()
        checkout_group.amount_retained=int(data['retained'])
        checkout_group.save()

        for participant in part_list:
            room=participant.room
            room.vacancy+=1
            room.save()
            participant.checkout_group=checkout_group
            participant.acco=False
            participant.save()

        encoded=generate_ckgroup_code(checkout_group)
        checkout_group.save()
        return redirect(reverse('regsoft:checkout_groups',kwargs={'c_id':college.id}))
    participant_list=Participant.objects.filter(acco=True)
    return render(request, 'regsoft/checkout.html', {'college':college, 'part_list':participant_list})

@staff_member_required
def master_checkout(request):
    ck_group_list=CheckoutGroup.objects.all()
    rows = [{'data':[ck_group.participant_set.all()[0].college.name,ck_group.participant_set.all().count(), ck_group.created_time, ck_group.amount_retained], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:ck_group_details', kwargs={'ck_id':ck_group.id})), 'title':'View Details'}]} for ck_group in ck_group_list]
    headings = ['College', 'Participant Count', 'Time of Checkout', 'Amount Retained', 'View Details']
    title = 'All Checkout groups'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title,
    }
    amount=0
    for ck_group in CheckoutGroup.objects.all():
        amount+=ck_group.amount_retained
    return render(request, 'regsoft/master_checkout.html', {'tables':[table,], 'amount':amount})

@staff_member_required
def checkout_groups(request, c_id):
    college = get_object_or_404(College, id=c_id)
    ck_group_list = [ck_group for ck_group in CheckoutGroup.objects.all() if ck_group.participant_set.all()[0].college == college]
    rows = [{'data':[ck_group.participant_set.all().count(), ck_group.created_time, ck_group.amount_retained], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:ck_group_details', kwargs={'ck_id':ck_group.id})), 'title':'View Details'}]} for ck_group in ck_group_list]
    headings = ['Participant Count', 'Time of Checkout', 'Amount Retained', 'View Details']
    title = 'Checkout groups from ' + college.name
    table = {
        'rows':rows,
        'headings':headings,
        'title':title,
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,]})

##Helper function to get event strings##
def get_event_string(participant):
    participation_set = MainParticipation.objects.filter(participant=participant, pcr_approved=True)
    events = ''
    for participation in participation_set:
        events += participation.event.name + ', '
    events = events[:-2]
    return events

@staff_member_required
def ck_group_details(request, ck_id):
    checkout_group = get_object_or_404(CheckoutGroup, id=ck_id)
    rows = [{'data':[part.name, part.phone, part.email, part.gender, get_event_string(part), part.room.room, part.room.bhavan.name], 'link':[]} for part in checkout_group.participant_set.all()]
    headings = ['Name', 'Phone', 'Email', 'Gender', 'Events', 'Room', 'Bhavan']
    title = 'Checkout detail at ' + str(checkout_group.created_time) + ', Amount Retained:' + str(checkout_group.amount_retained)
    table = {
        'rows':rows,
        'headings':headings,
        'title':title,
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,],})


################### CONTROLS ##################

@staff_member_required
def controls_home(request):
    rows=[]
    for group in Group.objects.all():
        code = group.group_code
        group_leader = get_group_leader(group)
        leader_name = group_leader.name
        leader_college = group_leader.college.name
        leader_phone = group_leader.phone
        time = group.created_time
        no_of_members = group.participant_set.filter(is_guest = False).count()
        controls_passed = group.participant_set.filter(controlz = True).count()
        bill_url = request.build_absolute_uri(reverse('regsoft:create_bill', kwargs={'g_id':group.id}))
        rows.append({
            'data': [
                code,
                leader_name,
                leader_college,
                leader_phone,
                time,
                no_of_members, 
                controls_passed
            ],
            'link': [{
                'url':bill_url,
                'title':'Create Bill'
            }]
        })
        print(rows)
        return HttpResponse(rows)

@staff_member_required
def create_bill(request,g_id):
    group=get_object_or_404(Group,id=g_id)
    controlz_passed=group.participant_set.filter(controlz=True,is_guest=False)
    controlz_unpassed=group.participant_set.filter(controlz=False,is_guest=False)
    if request.method=='POST':
        data=request.POST
        try:
            id_list=data.getlist('data')
        except:
            messages.warning(request,'Please select participants')
            return redirect(request.META.get('HTTP_REFERER'))
        if not id_list:
            messages.warning(request, 'Please select participants')
            return redirect(request.META.get('HTTP_REFERER'))
        bill = Bill()
        bill.two_thousands = data['twothousands']
        bill.five_hundreds = data['fivehundreds']
        bill.two_hundreds = data['twohundreds']
        bill.hundreds = data['hundreds']
        bill.fifties = data['fifties']
        bill.twenties = data['twenties']
        bill.tens = data['tens']
        bill.two_thousands_returned = data['twothousandsreturned']
        bill.five_hundreds_returned = data['fivehundredsreturned']
        bill.two_hundreds_returned = data['twohundredsreturned']
        bill.hundreds_returned = data['hundredsreturned']
        bill.fifties_returned = data['fiftiesreturned']
        bill.twenties_returned = data['twentiesreturned']
        bill.tens_returned = data['tensreturned']
        amount_dict = {'twothousands':2000, 'fivehundreds':500, 'twohundreds':200,'hundreds':100, 'fifties':50, 'twenties':20, 'tens':10}
        return_dict = {'twothousandsreturned':2000, 'fivehundredsreturned':500, 'twohundredsreturned':200,'hundredsreturned':100, 'fiftiesreturned':50, 'twentiesreturned':20, 'tensreturned':10}
        bill.amount=0
        for key,value in amount_dict.iteritems():
            bill.amount+=int(data[key])*int(value)
        for key,value in return_dict.iteritems():
            bill.amount-=int(data[key])*int(value)
        try:
            bill.draft_number=data['draft_number']
        except:
            pass
        bill.draft_amount=data['draft_amount']
        bill.amount+=int(bill.draft_amount)
        if not(bill.amount==0 and bill.draft_amount==0):
            bill.save()
            for p_id in id_list:
                part=Participant.objects.get(id=p_id)
                part.bill=bill
                part.controlz=True
                part.curr_controlz_paid=True
                part.curr_paid=True
                part.save()
            return redirect(reverse('regsoft:bill_details', kwargs={'b_id':bill.id}))
        else:
            messages.warning(request,'Please enter a bill amount')
            return redirect(reverse('regsoft:create_bill', kwargs={'g_id':group.id}))
    else:
        return render(request,'regsoft/controlz_group.html',{'controlz_passed':controlz_passed,'controlz_unpassed':controlz_unpassed,'group':group})


@staff_member_required
def show_all_bills(request):
    rows=[{'data':[college.name,college.participant_set.filter(controlz=True).count()],'link':[{'url':request.build_absolute_uri(reverse('regsoft:show_college_bills',kwargs={'c.id':college.id})),'title':'Show bills'}]} for college in College.objects.all()]
    headings=['College','Controlz passed participants','Show bills']
    title='Colleges for bill details'
    table={
        'rows':rows,
        'headings':headings,
        'title':title
    }
    return render(request,'regsoft/tables.html',{'tables':[table,]})


@staff_member_required
def show_college_bills(request,c_id):
    college=get_object_or_404(College,id=c_id)
    bills=[]
    for part in college.participant_set.filter(controlz=True):
        if part.bill not in bills:
            bills.append(part.bill)
    rows = [{'data':[bill.time_paid, bill.participant_set.filter(gender='male').count(), bill.participant_set.filter(gender='female').count(), bill.amount], 'link':[{'url':request.build_absolute_uri(reverse('regsoft:bill_details', kwargs={'b_id':bill.id})), 'title':'View Details'}]} for bill in bills]
    headings = ['Time Created', 'Male Participants', 'Female Participants', 'Amount', 'Details']
    title = 'Bills created for ' + college.name
    table = {
        'rows':rows,
        'headings':headings,
        'title':title
    }
    return render(request, 'regsoft/tables.html', {'tables':[table,]})

@staff_member_required
def bill_details(request,b_id):
    bill=get_object_or_404(Bill,id=b_id)
    from datetime import datetime
    time_stamp=datetime.now()
    participants=bill.participant_set.all()
    college=participants[0].college
    c_rows = [{'data':[part.name, get_event_string(part), bill.time_paid, get_amount(part)], 'link':[]} for part in bill.participant_set.all()]
    table = {
        'title' : 'Participant details for the bill from ' + college.name +'. Cash amount = Rs ' + str(bill.amount-bill.draft_amount) + '. Draft Amount = Rs ' + str(bill.draft_amount),
        'headings' : ['Name', 'Event(s)', 'Time created','Had to pay'],
        'rows':c_rows,
    }
    return render(request, 'regsoft/bill_details.html', {'tables':[table,],'bill':bill, 'participant_list':participants, 'college':college, 'curr_time':time_stamp})

def get_amount(participant):
    if participant.controlz_paid and participant.paid:
        return 0
    elif participant.paid:
        return 700
    else:
        return 1000

@staff_member_required
def print_bill(request,b_id):
    bill=get_object_or_404(Bill,id=b_id)
    from datetime import datetime
    time=datetime.now()
    participants=bill.participant_set.all()
    if not participants:
        return redirect(reverse('regsoft:bill_details', kwargs={'b_id':bill.id}))
    college=participants[0].college
    g_leader=bill.participant_set.all()[0].group.participant_set.get(is_g_leader=True)
    draft=bill.draft_number
    if not draft:
        draft='null'
    payment_methods=[{'method':'Cash','amount':bill.amount-bill.draft_amount},{'method':'Draft number '+draft,'amount':bill.draft_amount}]
    return render(request, 'regsoft/bill_invoice.html', {'bill':bill, 'part_list':participants, 'college':college, 'payment_methods':payment_methods, 'time':time, 'cr':g_leader})


@staff_member_required
def delete_bill(request,b_id):
    bill=get_object_or_404(Bill,id=b_id)
    participants=bill.participant_set.all()
    for part in participants:
        part.controlz=False
        part.curr_controlz_paid=False
        part.curr_paid=False
        part.save()
    bill.delete()
    college=participants[0].college
    return redirect(reverse('regsoft:show_college_bills',kwargs={'c_id':college.id}))
    