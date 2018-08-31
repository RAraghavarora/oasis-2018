from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from registrations.models import *
from events.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from functools import reduce
from registrations.urls import *
from registrations.views import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from oasis2018.settings import BASE_DIR
import sendgrid
import os
from sendgrid.helpers.mail import *
import xlsxwriter
from time import gmtime, strftime
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from oasis2018.keyconfig import *
import string
from random import choice

@staff_member_required
def index(request):
    return  redirect('pcradmin:college')

@staff_member_required
def college(request):
    rows = [{'data':[college.name,college.participant_set.filter(pcr_approved=True).count(),college.participant_set.filter(email_verified=True).count()],'link':[{'title':'Manage CR', 'url':reverse('pcradmin:select_college_rep', kwargs={'id':college.id})},{'title':'Approve Participations', 'url':reverse('pcradmin:approve_participations', kwargs={'id':college.id})}] } for college in College.objects.all()]
    tables=[{'title':'List of colleges',
    'rows':rows,'headings':['College','Confirmed','Total Particpants','Manage College Rep','Approve participations']}]
    return render(request, 'pcradmin/tables.html',{'tables':tables})


@staff_member_required
def select_college_rep(request,id):
    college=get_object_or_404(College,id=id)
    if request.method=='POST':
        data=request.POST
        try:
            part_id=data['data']
        except:
            messages.warning(request,'Select a participant')
            


