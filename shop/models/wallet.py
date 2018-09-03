import uuid as uuid_pylib
from django.db import models
from django.contrib.auth import User


class Wallet(models.Model):
    """ The main model where each (bitsian/participant/stall)'s money for the
		wallet will be stored. The E-wallet model. For stalls it denotes amount
		due to them, this way we can keep the Transaction model's to_wallet
		and not have to make an extra field like to_stall. DRY.
        It's composed of the Balance model for the reason of keeping the
        sources of money seperate. """

	PROFILES = (
			('bitsian', 'bitsian'),
			('participant', 'participant'),
			('stall', 'stall')
	)

	user = models.OneToOneField(User, on_delete=models.set_null, null=True)
    uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=false)
    phone = models.BigIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    profile = models.CharField(max_length=16, choices=PROFILES)
    timestamp = models.DateTimeField(auto_add_now=True)
	# transferred_in: Transactions
	# transferred_out: Transactions
	# orders: Orders
	# cart: Cart

    def __str__(self):
        text = "{}'s wallet"
        try:
            profile = self.getProfile()
			if not profile:
				raise
			else:
				return text.format(profile.name)
        except:
            return (str(self.uid))

	def getProfile(self):
		try:
	        if self.profile == "bitsian":
				return self.user.bitsian
			elif self.profile == "participant":
				return self.user.participant
			elif self.profile == "stall":
				return self.user.stall
			raise
		except:
			return None
