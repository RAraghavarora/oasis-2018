import csv
from shop.models import *
from django.contrib.auth.models import User
from oasis2018.settings import BASE_DIR


with open(BASE_DIR + '/utils/STALLS-MENU.csv') as cfile:
    reader = csv.reader(cfile, delimiter=',')
    for row in reader:
        try:
            stall = Stall.objects.get(name=row[0])
        except Stall.DoesNotExist:
            user, created = User.objects.get_or_create(username=row[0])
            stall = Stall.objects.create(user=user, name=row[0])
        ItemClass.objects.create(name=row[1], stall=stall, price=int(row[2]), )