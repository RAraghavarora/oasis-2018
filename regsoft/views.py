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

##Helper function to get group leader##
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
    
                    