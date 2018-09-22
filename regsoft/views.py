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
from pcradmin.views import get_cr_name, gen_barcode, get_pcr_number
from django.contrib import messages
from django.contrib.auth.models import User
import sendgrid
import os
import re   
from sendgrid.helpers.mail import *
from oasis2017.keyconfig import *
import string
from random import sample, choice
from django.contrib import messages 


#########Recnacc#########

##Helper function to get the group leader##
def get_group_leader(group):
    return group.participant_set.get(is_g_leader=True)

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
        from datetime import *
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
