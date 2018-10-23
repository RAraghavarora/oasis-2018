import csv
from shop.models import *
from oasis2018.settings import BASE_DIR


with open(BASE_DIR + '/utils/data.csv') as cfile:
 ew = csv.reader(cfile, delimiter=',')
 for r in ew:
  try:
   s=Stall.objects.get(name=r[-1])
  except:
  	u, c = User.objects.get_or_create(username=r[-1])
  	s = Stall.objects.create(user=u, name=r[-1])
  ItemClass.objects.create(name=r[0], stall=s, price=r[1], )