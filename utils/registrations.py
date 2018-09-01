from registrations.models import Participant
from django.http import HttpResponse
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