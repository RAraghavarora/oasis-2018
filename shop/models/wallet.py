import uuid as uuid_pylib
from django.db import models
from django.contrib.auth.models import User
from shop.models.balance import Balance
from shop.models.transaction import Transaction


class Wallet(models.Model):
	""" The main model where each (bitsian/participant/stall)'s money for the
		wallet will be stored. The E-wallet model. For stalls it denotes amount
		due to them, this way we can keep the Transaction model's to_wallet
		and not have to make an extra field like to_stall. DRY.
		It's composed of the Balance model for the reason of keeping the
		sources of money seperate. """

	PROFILES = (
			('B', 'bitsian'),
			('P', 'participant'),
			('S', 'stall')
	)

	user = models.OneToOneField(User, related_name = 'wallet', on_delete=models.SET_NULL, null=True)
	uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=False)
	phone = models.BigIntegerField(default=0)
	balance = models.OneToOneField("Balance", on_delete=models.CASCADE, blank=True, null=True)
	profile = models.CharField(max_length=1, choices=PROFILES)
	timestamp = models.DateTimeField(auto_now_add=True)
	# transferred_in: Transactions
	# transferred_out: Transactions
	# orders: Orders

	def __str__(self):
		text = "{}'s Wallet"
		try:
			profile = self.getProfile()
			if not profile:
				raise
			else:
				return text.format(profile.name)
		except:
			return (str(self.uuid))

	def getProfile(self):
		try:
			if self.profile == "B":
				return self.user.bitsian
			elif self.profile == "P":
				return self.user.participant
			elif self.profile == "S":
				return self.user.stall
			raise
		except:
			return None

	def getTotalBalance(self):
		return self.balance._getTotal()

	def transferTo(self, target_wallet, amount, transfertype):
		self.balance.deduct(amount)
		target_wallet.balance.add(0,0,0,amount)
		Transaction.objects.create(
									amount = amount,
									transfer_to = target_wallet,
									transfer_from = self,
									transfer_type = transfertype,
									refund_id = ""
								)
