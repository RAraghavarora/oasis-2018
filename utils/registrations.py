from django.http import HttpResponse

from registrations.models import Participant

import qrcode
from random import choice


def generate_email_token(participant):
	'''
	To generate a unique email token for a registering participant
	'''
	import uuid
	token = uuid.uuid4().hex
	registered_tokens = [profile.email_token for profile in Participant.objects.all()]

	while token in registered_tokens:
		token = uuid.uuid4().hex

	participant.email_token = token
	participant.save()

	return token 

def authenticate_email_token(token):
	'''
	To authenticate the token registered to a participant while verifying email
	'''
	try:
		participant = Participant.objects.get(email_token=token)
		participant.email_verified = True
		participant.save()
		return participant
	except :
		return False

def get_pcr_number():
	number_list = [8003305723,7972812406,8108259735,8412970942]
	from random import randint
	return number_list[randint(0,3)]

def resize_uploaded_image(buf, height, width):
	'''
	To resize the uploaded image
	'''
	
	import StringIO
	from PIL import Image
	image = Image.open(buf)
	width = width
	height = height
	resizedImage = image.resize((width, height))

	# Turn back into file-like object
	resizedImageFile = StringIO.StringIO()
	resizedImage.save(resizedImageFile , 'JPEG', optimize = True)
	resizedImageFile.seek(0)    # So that the next read starts at the beginning

	return resizedImageFile

# def gen_barcode(part):
# 	chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# 	part_id=part.id
# 	encoded=part.barcode
# 	if encoded=='':
# 		raise ValueError
# 	while 1:
# 		encoded = ''.join(choice(chars) for _ in range(8))
# 		barcode = 'oasis17' + encoded
# 		if not Participant.objects.filter(barcode=barcode):
# 			break
# 	part.barcode = barcode
# 	part.save()

# 	part_code = qrcode.make(part.barcode)
# 	try:
# 		image='/root/live/oasis/backend/resources/oasis2017/qrcodes/%04s.png' % int(part_id)
# 		part_code.save(image, 'PNG')
# 	except:
# 		image = '/home/sanchit/Desktop/%04s.png' % int(part_id)
# 		part_code.save(image, 'PNG')
# 	return encoded

def generate_qr_code(data):
	import qrcode
	import qrcode.image.svg
	from PIL import Image

	part_code = qrcode.make(data)
	part_code = part_code.resize([30, 30])
	# import qrcode.image.svg
	# from PIL import Image
	# part_code = 
	return part_code