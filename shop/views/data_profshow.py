from shop.models.transaction import *
from shop.models.item import *
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout


# @staff_member_required
# def user_logout(request):
# 	logout(request)
# 	return HttpResponse("You are logged out")

@staff_member_required
def get_data(request):
    profsigned_list=[profs for profs in Tickets.objects.all() if profs.count!=0]
    print(profsigned_list)
    rows=[{'data':[profsigned_list.user.participant.name,profsigned_list.prof_show,]
    headings=['Participant Name','Prof Show Signed',]
    title='Data'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title
    }
    return render(request, 'shop/tables.html', {'tables':[table,]})