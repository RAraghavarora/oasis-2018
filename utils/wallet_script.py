from registrations.models import *
from events.models import *
from shop.models.wallet import Wallet

for i in Group.objects.all():
    for x in i.participant_set.all():
        if x.firewallz_passed:
            wallet, created = Wallet.objects.get_or_create(user=x.user, profile="P")
            if created:
                balance = Balance.objects.create(wallet=wallet)
                wallet.balance = balance
                wallet.save()

            
