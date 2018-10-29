from registrations.models import *
from shop.models.item import Tickets
import sys
import csv
from shop.models import *
# from openpyxl import *
# filename2='/home/sanchit/DVM_SHIT/oasis-2018/scripts/SEL and EDM signings sheet Pre-Oasis.xlsx'
# f1 = '/home/sanchit/DVM_SHIT/oasis-2018/scripts/FINAL STUDENT LIST.xlsx'
# wb = load_workbook(filename=filename2)
# sheet = wb["Sheet1"]
# wb2 = load_workbook(filename=f1)
# sheet2 = wb2['MASTERSHEET'] #Student list
# length = len(tuple(sheet.rows))

p1 = MainProfShow.objects.get(name__icontains="shankar")
p2 = MainProfShow.objects.get(name__icontains="edm")

cnt=0
with open("scripts/eggs.csv") as f:
    wb = csv.reader(f)
    for row in wb:
        email = row[0]
        try:
            a = int(row[1])
        except:
            a=0
        try:
            b = int(row[2])
        except:
            b=0
        try:
            c = int(row[3])
        except:
            c=0

        a+=c
        b+=c
        try:
            bit = Bitsian.objects.get(email=email)
        except:
            continue
        try:
            user = bit.user
        except:
            continue
        if a>0:
            try:
                t = Tickets.objects.get(prof_show=p1, user=user)
                t.count += a
                t.save()
            except:
                t =  Tickets.objects.create(prof_show=p1, user=user, count = a)
        if b>0:
            try:
                t = Tickets.objects.get(prof_show=p2, user=user)
                t.count += b
                t.save()
            except:
                t =  Tickets.objects.create(prof_show=p2, user=user, count = b)
        cnt+=1

print(cnt)