from shop.models.item import *
from events.models import *

for i in Tickets.objects.all():
    if i.is_excel_sheet==True:
        i.delete()