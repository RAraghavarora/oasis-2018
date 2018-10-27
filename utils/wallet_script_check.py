from registrations.models import *
from events.models import *
from shop.models.wallet import Wallet
from shop.models.balance import Balance

for i in Group.objects.all():
    for x in i.participant_set.all():
        if x.firewallz_passed and not x.user.wallet:
            print(x.email)