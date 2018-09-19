import json

from django.dispatch import receiver
from django.db.models.signals import post_save

from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.stall import Stall
from registrations.models import Bitsian
from registrations.models import Participant


@receiver(post_save, sender=Stall)
def autoAddWalletStall(sender, **kwargs):
    if kwargs["created"]:
        stall = kwargs["instance"]
        wallet = Wallet.objects.create(user=stall.user, profile="S")
        # Now give the wallet a balance. This has to be done seperately because
        # of a the BalanceFirebaseUpdate signal which uses self.wallet.user.id
        balance = Balance(wallet=wallet)
        balance.save()
        # these next two steps are needed... tested.
        wallet.balance = balance
        wallet.save()


@receiver(post_save, sender=Bitsian)
def autoAddWalletBitsian(sender, **kwargs):
    if kwargs["created"]:
        bitsian = kwargs["instance"]
        wallet = Wallet.objects.create(user=bitsian.user, profile="B")
        balance = Balance(wallet=wallet)
        balance.save()
        wallet.balance = balance
        wallet.save()


@receiver(post_save, sender=Participant)
def autoAddWalletParticipant(sender, **kwargs):
    if participant.firewallz_passed:
        participant = kwargs["instance"]
        wallet = Wallet.objects.create(user=participant.user, profile="P")
        balance = Balance(wallet=wallet)
        balance.save()
        wallet.balance = balance
        wallet.save()
