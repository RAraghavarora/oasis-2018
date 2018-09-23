from django.http import JsonResponse
from oasis2018 import loggers
import logging

logger = logging.getLogger('wallet')

def test(request):
	if request.method == 'GET':
		logger.info('Test view was processed!')
		return JsonResponse({'status':'success'})