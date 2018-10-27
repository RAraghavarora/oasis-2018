from registrations.models import Bitsian
from django.contrib.auth.models import User
from shop.models.item import *
from events.models import *
# from shop.models.transaction import *
from openpyxl import *
# from random import *
_dir='/home/sanchit/Downloads/'
wb = load_workbook(_dir + 'Guthrie Govan signings.xlsx',data_only=True)
sheet2=wb['Google form']
sheet1 = wb['actual']



length1 = len(tuple(sheet1.rows))
length2 = len(tuple(sheet2.rows))
length3=length1+length2
id1=[]
id2=[]
cnt=0
for i in range(2,length1):
    bits_id1=sheet1.cell(row=i,column=6).value
    id1.append(bits_id1)
for i in range(2,length2):
    bits_id2=sheet2.cell(row=i,column=4).value
    bits_id2=bits_id2[:-1]
    id2.append(bits_id2)
final_id=id1+id2
for i in range(1,length3):
    bitisian=Bitsian.objects.get(long_id=final_id[i])
    prof_show=MainProfShow.objects.get(id=1)
    Tickets.objects.get_or_create(prof_show=prof_show,user=bitsian.user,count=1)
    print("obj1 "+str(i))

    
    
   
    


