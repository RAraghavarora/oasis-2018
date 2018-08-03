import traceback

from django.utils.deprecation import MiddlewareMixin

from . import sg

class AppException(MiddlewareMixin):
    
    def process_exception(self, request, exception):
        exception = str(exception)
        email = sg
        email.con +=    "Request method:" + request.META['REQUEST_METHOD'] + \
                        request.META['PATH_INFO'] + request.META['QUERY_STRING'] + request.META['REMOTE_ADDR'] + \
                        '\n' + "Error message is :" + exception + \
                        '\n' + traceback.format_exc()
		print email.con                        
        email.send_email()
        return None
        
        
