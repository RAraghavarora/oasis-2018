from oasis2018.settings import BASE_DIR
from registrations.models import Bitsian
from django.contrib.auth.models import User
from openpyxl import load_workbook
import csv

filename = BASE_DIR + "/utils/student_list.xlsx"
wb = load_workbook(filename=filename)
sheet = wb["MASTERSHEET"]

length = len(tuple(sheet.rows))

for i in range(2, length):

	long_id = sheet.cell(row=i, column=2).value
	email = sheet.cell(row=i, column=3).value
	name = sheet.cell(row=i, column=4).value.title()
	room_no = int(sheet.cell(row=i, column=5).value)
	bhawan = sheet.cell(row=i, column=6).value
	print(long_id, email, name, room_no, bhawan)
	try:
		user=User.objects.get(username=email.split('@')[0])
	except:
		user=User.objects.create(username=email.split('@')[0])
	try:
		Bitsian.objects.get(user=user, name=name, long_id=long_id, room_no=room_no, bhawan=bhawan, email=email)
	except:
		Bitsian.objects.create(user=user, name=name, long_id=long_id, room_no=room_no, bhawan=bhawan, email=email)
