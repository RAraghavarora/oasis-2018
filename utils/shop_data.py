import csv
from shop.models.item import ItemClass
from shop.models.stall import Stall
from django.contrib.auth.models import User
from oasis2018.settings import BASE_DIR

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pep.settings')

import django
django.setup()

def execute():
	with open(BASE_DIR + '/utils/STALLS MENU.csv') as cfile:
		reader = csv.reader(cfile, delimiter=',')
		for row in reader:
			try:
				stall = Stall.objects.get(name=row[-1])
			except Stall.DoesNotExist:
				user, created = User.objects.get_or_create(username=row[-1])
				stall = Stall.objects.create(user=user, name=row[-1])
			ItemClass.objects.create(name=row[0], stall=stall, price=row[1], )
