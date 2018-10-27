from oasis2018.settings import BASE_DIR
from registrations.models import Bitsian
from django.contrib.auth.models import User
from shop.models.item import *
from events.models import *
# from shop.models.transaction import *
from openpyxl import *
# from random import *
filename = BASE_DIR + "/scripts/Guthrie Govan signings.xlsx"
wb = load_workbook(filename=filename,data_only=True)
sheet2=wb['Google form']
sheet1 = wb['actual']



length1 = len(tuple(sheet1.rows))
length2 = len(tuple(sheet2.rows))
for i in range(2,length1):
    bits_id1=sheet1.cell(row=i,column=2).value
    #print(bits_id1)
    try:
        bitsian=Bitsian.objects.get(long_id=bits_id1)
        prof_show=MainProfShow.objects.get(id=1)    
        Tickets.objects.get_or_create(prof_show=prof_show,user=bitsian.user,count=1)
        print("obj1 "+str(i))
    except:
        pass
for i in range(2,length2):
    try:
        bits_id2=sheet2.cell(row=i,column=4).value
        bits_id2=bits_id2[:-1]
        bitsian=Bitsian.objects.get(long_id=bits_id2)
        prof_show=MainProfShow.objects.get(id=1)    
        Tickets.objects.get_or_create(prof_show=prof_show,user=bitsian.user,count=1)
        print("obj2 "+str(i))
    except:
        pass

    
    
   
    


