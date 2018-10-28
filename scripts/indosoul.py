
from openpyxl import *
# from oasis2018.settings import BASE_DIR
# from registrations.models import Bitsian
# from django.contrib.auth.models import User
# from shop.models.item import *
# from events.models import *
# from shop.models.transaction import *
# from random import *
# filename = BASE_DIR + "/scripts/IndoSoul DVM.xlsx"
filename2='/home/sanchit/Downloads/IndoSoul DVM.xlsx'
wb = load_workbook(filename=filename2,data_only=True)
sheet1=wb['Sheet1']
length1 = len(tuple(sheet1.rows))
print("hello")
for i in range(3,10):
    bits_id1=sheet1.cell(row=i,column=1).value
    count=int(sheet1.cell(row=i,column=3).value)
    print(bits_id1)
    try:
        
        bitsian=Bitsian.objects.get(long_id=bits_id1)
        profshow=MainProfShow.objects.get(name="Indosoul")
        try:
            t = Tickets.objects.get(prof_show=profshow,user=bitsian.user)
            t.count+=count
            t.save()
        except:
            Tickets.objects.create(prof_show=profshow,user=bitsian.user, count=count)
        cnt+=1
        print("obj"+str(cnt))
    
    except:
        pass


# profshow=MainProfShow.objects.get(id=7)