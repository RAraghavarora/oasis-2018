import io
import json

from Custom.errors import ContentTypeError, InvalidCredentialsError, InvalidPermissionsError

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import *

from events.models import *
from preregistration.models import *

@csrf_exempt
def IntroEventsData(request):

    if request.method == "GET":
        return render(request, "events/IntroEventsData.html")

    if request.method == "POST":

        try:
            # STEP 1: receive the username and password from the request based on content_type
            content_type = request.META["CONTENT_TYPE"].split(";")[0]
            if content_type == "application/x-www-form-urlencoded" or content_type == "multipart/form-data":
                username = request.POST["username"]
                password = request.POST["password"]
            elif content_type == "application/json":
                json_data = json.loads(request.body.decode("utf-8"))
                username = json_data["username"]
                password = json_data["password"]
            else:
                raise ContentTypeError()

            # STEP 2: check database for user and is an event user
            event_user = authenticate(username=username, password=password)
            if not event_user:
                raise InvalidCredentialsError()
            try: # check to see if the user is associated with an event
                event = event_user.eventmodel
            except Exception:
                raise InvalidPermissionsError()

            # STEP 3: Excel Sheet Generation Step after Authentication
            databook = Workbook()
            datasheet = databook.active
            datasheet.title = "{} Data".format(username)

            datasheet["A1"] = "Name"
            datasheet.column_dimensions["A"].width = 20
            datasheet["B1"] = "PCR Approval"
            datasheet.column_dimensions["B"].width = 15
            datasheet["C1"] = "CR Approval"
            datasheet.column_dimensions["C"].width = 15
            datasheet["D1"] = "Email Address"
            datasheet.column_dimensions["D"].width = 30
            datasheet["E1"] = "Phone Number"
            datasheet.column_dimensions["E"].width = 15

            counter = 2
            for participation in event.participation.all():
                datasheet["A{}".format(counter)] = participation.participant.name
                if participation.pcr_approved:
                    datasheet["B{}".format(counter)] = "Approved"
                else:
                    datasheet["B{}".format(counter)] = "Not Approved"
                if participation.cr_approved:
                    datasheet["C{}".format(counter)] = "Approved"
                else:
                    datasheet["C{}".format(counter)] = "Not Approved"
                datasheet["D{}".format(counter)] = participation.participant.email_address
                datasheet["E{}".format(counter)] = participation.participant.phone
                counter += 1

            # STEP 4: prepare the response and return the document
            response = HttpResponse(content=save_virtual_workbook(databook), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename={}".format("{}Data.xlsx".format(username))
            return response

        except KeyError as missing_data:
            return JsonResponse({"error_message":"missing credentials in request: {}".format(missing_data)})

        except ContentTypeError:
            return JsonResponse({"error_message":"INVALID TYPE: {}".format(content_type)})

        except InvalidCredentialsError:
            return JsonResponse({"error_message":"Invalid Credentials."})

        except InvalidPermissionsError:
            return JsonResponse({"error_message":"Invalid Permissions"})
