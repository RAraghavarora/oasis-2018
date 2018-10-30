from shop.models.transaction import *
from shop.models.item import *
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout



def user_logout(request):
 	logout(request)
 	return HttpResponse("You are logged out")


def get_data(request):
    profsigned_list=[profs for profs in Tickets.objects.all()]
    print(profsigned_list)

    rows=[{'data':[shows.user.bitsian.name,shows.prof_show,shows.tickettransaction.get(tickets=shows).timestamp,shows.tickettransaction.get(tickets=shows).num]} for shows in profsigned_list]
    headings=['Participant Name','Prof Show Signed','Timestamp','Tickets Consumed']
    title='Data'
    table = {
        'rows':rows,
        'headings':headings,
        'title':title
    }
    return render(request, 'shop/tables.html', {'tables':[table,]})

