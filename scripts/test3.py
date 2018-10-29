import sys
from openpyxl import *
filename='scripts/soul.xlsx'
wb = load_workbook(filename=filename)
sheet = wb["Sheet1"]
print(sheet.cell(row=1, column=3).value)