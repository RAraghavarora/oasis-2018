import json
import time

from django.dispatch import receiver
from django.db.models.signals import post_save

from utils.wallet_qrcode import genString
from shop.models.wallet import Wallet
from shop.models.balance import Balance
from shop.models.stall import Stall
from registrations.models import Bitsian
from registrations.models import Participant
from shop.models.teller import Teller


@receiver(post_save, sender=Stall)
def autoAddWalletStall(sender, **kwargs):
    try:
        if kwargs["created"]:
            stall = kwargs["instance"]
            wallet, created = Wallet.objects.get_or_create(user=stall.user, profile="S")
            if created:
                balance = Balance.objects.create(wallet=wallet)
                wallet.balance = balance
                wallet.save()
    except:
        time.sleep(1)
        autoAddWalletStall(sender, **kwargs)


@receiver(post_save, sender=Bitsian)
def autoAddWalletBitsian(sender, **kwargs):
    try:
        if kwargs["created"]:
            bitsian = kwargs["instance"]
            bitsian.barcode = genString(bitsian.user.id, bitsian.email)
            bitsian.save()
            wallet, created = Wallet.objects.get_or_create(user=bitsian.user, profile="B")
            if created:
                balance = Balance.objects.create(wallet=wallet)
                wallet.balance = balance
                wallet.save()
    except:
        time.sleep(1)
        autoAddWalletBitsian(sender, **kwargs)


@receiver(post_save, sender=Participant)
def autoAddWalletParticipant(sender, **kwargs):
    try:
        participant = kwargs["instance"]

        if participant.firewallz_passed:
            if not participant.barcode:
                participant.barcode = genString(participant.user.id, participant.email)
                participant.save()
            wallet, created = Wallet.objects.get_or_create(user=participant.user, profile="P")
            if created:
                balance = Balance.objects.create(wallet=wallet)
                wallet.balance = balance
                wallet.save()
    except:
        time.sleep(1)
        autoAddWalletParticipant(sender, **kwargs)


@receiver(post_save, sender=Teller)
def autoAddWalletTeller(sender, **kwargs):
    try:
        if kwargs["created"]:
            teller = kwargs["instance"]
            wallet, created = Wallet.objects.get_or_create(user=teller.user, profile="T")
            if created:
                balance = Balance.objects.create(wallet=wallet)
                wallet.balance = balance
                wallet.save()
    except:
        time.sleep(1)
        autoAddWalletTeller(sender, **kwargs)
