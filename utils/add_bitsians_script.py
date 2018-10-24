from oasis2018.settings import BASE_DIR
from registrations.models import Bitsian
from openpyxl import load_workbook
import csv

filename = BASE_DIR + "/utils/student_list.xlsx"
wb = load_workbook(filename=filename)
ws = wb["MASTERSHEET"]

length = len(tuple(ws.rows))

for i in range(2, length):

	long_id = sheet.cell(row=i, column=2).value
	email = sheet.cell(row=i, column=3).value
	name = sheet.cell(row=i, column=4).value
	room_no = int(sheet.cell(row=i, column=5).value)
	bhawan = sheet.cell(row=i, column=6).value

	Bitsian.objects.create(name=name, long_id=long_id, room_no=room_no, bhawan=bhawan, email=email)