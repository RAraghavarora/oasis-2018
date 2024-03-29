import os
import datetime
import traceback

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from . import sg

class AppException(MiddlewareMixin):

    def process_exception(self, request, exception):
        exception = str(exception)
        email = sg
        email.con += "Request method:" + request.META['REQUEST_METHOD'] + \
        request.META['PATH_INFO'] + request.META['QUERY_STRING'] + request.META['REMOTE_ADDR']
        email.con += '\n' + "Error message is :" + exception + '\n' + traceback.format_exc()
        email.send_email()
        return None