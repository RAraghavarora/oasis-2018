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