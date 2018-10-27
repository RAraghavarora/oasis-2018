import csv
from shop.models import *
from django.contrib.auth.models import User
from oasis2018.settings import BASE_DIR


with open(BASE_DIR + '/utils/stalls_menu2.csv') as cfile:
    reader = csv.reader(cfile, delimiter=',')
    for row in reader:
        try:
            stall = Stall.objects.get(name=row[-1])
        except Stall.DoesNotExist:
            user, created = User.objects.get_or_create(username=row[-1])
            stall = Stall.objects.create(user=user, name=row[-1])
    ItemClass.objects.create(name=row[0], stall=stall, price=row[1], )