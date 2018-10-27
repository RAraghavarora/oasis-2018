while True:
	a = input()
	b = a.split('@')[0]
	c = a.split('@')[1]
	if b[4] != '8' and b[4] != '7':
		email = b[0:5] + b[6:] + c
		print(email)
	else:
		print(a)