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
        email.con +=    "Request method:" + request.META['REQUEST_METHOD'] + \
                        request.META['PATH_INFO'] + request.META['QUERY_STRING'] + request.META['REMOTE_ADDR'] + \
                        '\n' + "Error message is :" + exception + \
                        '\n' + traceback.format_exc()
        email.send_email()
        return None


class RRLoggerMiddleWare():
    """ A bit of middleware to log requests and responses when an error has been raised,
        this must be the last middleware in the middlewares list. """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if  response.status_code > 308 :
            log_path = os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'rrlog.log')
            if not os.path.exists(log_path):
                os.mkdir(log_path.rsplit('/', 1)[0])


            with open(log_path, 'a+') as logfile:
                dt = datetime.datetime.now()
                logfile.write("DATE: {}/{}/{}\n".format(dt.year, dt.month, dt.day))
                logfile.write("TIME: {}:{}\n".format(dt.hour, dt.minute))
                logfile.write("URI:" + request.path + "\n")
                logfile.write("REQUEST BODY:\n{}\n".format(request.body))


                logfile.write("RESPONSE: {}\n{}\n\n".format(response.status_code, response))

        return response
