from django.db import models


class Balance(models.Model):
	"""
	There are 4 sources of money for each wallet, and it is essential that
	we keep the 4 sources seperate. SWD money must be refunded while other
	money will be lost at the end (the user SHOULD and will be warned).
	"""
	swd = models.PositiveIntegerField(default=0)
	cash = models.PositiveIntegerField(default=0)
	instamojo = models.PositiveIntegerField(default=0)
	transfers = models.PositiveIntegerField(default=0)

	# wallet: Wallet

	def __str__(self):
		#ret_string = "{}'s Wallet - ".format(self.wallet.user.username) + \
		#	"Balance: {}/{}/{}/{}".format(self.swd, self.cash, self.instamojo, self.transfers)
		#return ret_string
		return "Balance: {}/{}/{}/{}".format(self.swd, self.cash, self.instamojo, self.transfers)

	def _getTotal(self):
		return self.swd + self.cash + self.instamojo + self.transfers

	def add(self, swd=0, cash=0, instamojo=0, transfers=0):
		if all([swd>=0, cash>=0, instamojo>=0, transfers>=0]):
			self.swd += swd
			self.cash += cash
			self.instamojo += instamojo
			self.transfers += transfers
			self.save()
		else:
			# log it as Warning and handle it.
			raise

	def deduct(self, amount):
		"""
		first deduct money from transfers, then instamojo, then cash and
		most importantly at the VERY END deduct from SWD. This is because
		SWD money can be refunded.
		"""
		# first check for sufficient balance
		if self._getTotal() < amount:
			raise
			# log it, and act accordingly

		# now proceed to reduce amount.
		money = 0
		# we will add to "money" from the sources in order
		# until the "amount" is achieved

		if self.transfers < amount:
			money += self.transfers
			self.transfers = 0
			if self.instamojo + money < amount:
				money += self.instamojo
				self.instamojo = 0
				if self.cash + money < amount:
					money += self.cash
					self.cash = 0
					if self.swd + money < amount:
						money += self.swd
						self.swd = 0
					else:
						self.swd -= amount-money
						money += amount
				else:
					self.cash -= amount-money
					money += amount
			else:
				self.instamojo -= amount-money
				money += amount
		else:
			self.transfers -= amount
			money += amount

		self.save()
		# log
