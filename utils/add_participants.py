from oasis2018.settings import BASE_DIR
from registrations.models import Bitsian
from django.contrib.auth.models import User
from openpyxl import load_workbook
import csv

filename = BASE_DIR + "/utils/student_list3.xlsx"
# filename2='/home/sanchit/Downloads/student_list2.xlsx'
wb = load_workbook(filename=filename)
sheet = wb["MASTERSHEET"]

