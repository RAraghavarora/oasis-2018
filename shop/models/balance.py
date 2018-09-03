from django.db import models


class Balance(models.Models):
	""" There are 4 sources of money for each wallet, and it is essential that
		we keep the 4 sources seperate. SWD money must be refunded while other
		money will be lost at the end (the user SHOULD and will be warned)."""
		swd = models.PositiveIntegerField(default=0)
		cash = models.PositiveIntegerField(default=0)
		instamojo = models.PositiveIntegerField(default=0)
		transfers = models.PositiveIntegerField(default=0)

		def __str__(self):
			return("{}/{}/{}/{}".format(swd, cash, instamojo, transfers))
