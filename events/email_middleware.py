from django.utils.deprecation import MiddlewareMixin
from . import sg
import traceback

class AppException(MiddlewareMixin):
    
    def process_exception(self, request, exception):
        a = str(exception)
        email = sg
        email.con = email.con +  a +'\n' + traceback.format_exc()
        email.send_email()
        return None
        