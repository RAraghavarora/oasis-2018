from shop.models.stall import stall

stalls = Stall.objects.all()

for stall in stalls:
	try:
		for item in stall.menu.all():
			item.save()
		stall.user.wallet.balance.save()
		for order in stall.orders.all():
			order.save()
	except Exception as e:
		print(e)