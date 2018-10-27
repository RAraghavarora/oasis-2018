from openpyxl import *
from shop.models import *

filename = BASE_DIR + "/utils/student_list2.xlsx"
filename2='/home/sanchit/Downloads/STALLS MENU.xlsx'
wb = load_workbook(filename=filename)
sheet = wb["Sheet1_2"]
length = len(tuple(sheet.rows))

for i in range(2,length):
    stall_name=sheet.cell(row=i,column=1).value
    item_name=sheet.cell(row=i,column=2).value
    price=sheet.cell(row=i,column=3).value
    
