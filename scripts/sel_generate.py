import sys
from openpyxl import *
filename2='/home/sanchit/DVM_SHIT/oasis-2018/scripts/SEL and EDM signings sheet Pre-Oasis.xlsx'
f1 = '/home/sanchit/DVM_SHIT/oasis-2018/scripts/student_list3.xlsx'
wb = load_workbook(filename=filename2)
sheet = wb["Sheet1"]
wb2 = load_workbook(filename=f1)
sheet2 = wb2['MASTERSHEET'] #Student list
length = len(tuple(sheet.rows))
emailist=[]
long_list=[]
idd_list=[]
l=[]
l2 = len(tuple(sheet2.rows))
p = []
for j in range(2, l2):
    idd = sheet2.cell(row=j, column=2).value
    ee = sheet2.cell(row=j, column=10).value
    p.append([ee, idd])
    idd_list.append(idd)
dick = {idd: ee for ee, idd in p}
#print(len(dick))

for i in range(2, length):

    un= str(sheet.cell(row=i,column=1).value)
    long_id = sheet.cell(row=i, column=1).value
    long_list.append(long_id)
    try:
        l.append(dick[long_id])
        
    except:
        pass

print(len(l))


