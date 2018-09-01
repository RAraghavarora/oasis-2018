import io
import json

from utils.errors import ContentTypeError, InvalidCredentialsError, InvalidPermissionsError

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
from events.extrafunctions.generations import *

@csrf_exempt
def Data(request):

    if request.method == "GET":
        return render(request, "events/data.html")

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
            datasheet.title = "{} Data".format(event.name)
  # defined in ./extrafunctions/generations.py
            if event.name == "RapWars":
                RapWarsGeneration(datasheet)
            elif event.name== "PurpleProse":
                PurpleProseGeneration(datasheet)
            elif event.name=="StandupSoapbox":
                StandupSoapboxGeneration(datasheet)
            elif event.name == "Rocktaves" or event.name == "Roctaves":
                RocktavesGeneration(datasheet)
            else:
                return JsonResponse({"error_message":"Event Invalid."})

            # STEP 4: prepare the response and return the document
            response = HttpResponse(content=save_virtual_workbook(databook), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename={}".format("{}Data.xlsx".format(event.name))
            return response

        except KeyError as missing_data:
            return JsonResponse({"error_message":"missing credentials in request: {}".format(missing_data)})

        except ContentTypeError:
            return JsonResponse({"error_message":"INVALID TYPE: {}".format(content_type)})

        except InvalidCredentialsError:
            return JsonResponse({"error_message":"Invalid Credentials."})

        except InvalidPermissionsError:
            return JsonResponse({"error_message":"Invalid Permissions"})
