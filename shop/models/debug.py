from django.db import models


class DebugInfo(models.Model):

	ANDROID = 'A'
	IOS = 'I'
	WEB = 'W'
	SERVER = 'S'

	IDENTITY = (
		(ANDROID, "Android"),
		(IOS, "IOS"),
		(WEB, "Web"),
		(SERVER, "Server"),
	)

	identity = models.CharField(max_length = 1, choices=IDENTITY)
	debug_info = models.CharField(max_length = 10000)
	timestamp = models.DateTimeField(auto_now = True)

	def __str__(self):
		return "{} : {}".format(self.get_identity_display(), str(self.timestamp))