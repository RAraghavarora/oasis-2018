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

from .models import *


@csrf_exempt
def IntroEventsData(request):

    if request.method == "GET":
        return render(request, "events/IntroEventsData.html")

    if request.method == "POST":
        # Authentication Step:
        try:
            # receive the username and password accordingly
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

            # check database for user and act accordingly
            user = authenticate(username=username, password=password)
            if not user:
                raise InvalidCredentialsError()
            if not user.is_staff:
                raise InvalidPermissionsError()

            # Excel Sheet Generation Step after Authentication
            wb = Workbook()
            ws = wb.active
            ws.title = "Events Data"

            # set title row
            ws["A1"] = "Name"
            ws["B1"] = "Short Description"
            """increase the column width -> pending"""
            ws["C1"] = "Rules"
            ws["D1"] = "Category"
            ws["E1"] = "Contact"

            # now fill Data
            counter = 1
            for event in IntroEvent.objects.all():
                counter += 1
                ws["A{}".format(counter)] = event.name
                ws["B{}".format(counter)] = event.short_description
                ws["C{}".format(counter)] = event.rules
                ws["D{}".format(counter)] = event.category.name
                ws["E{}".format(counter)] = event.contact

            # return the document
            response = HttpResponse(content=save_virtual_workbook(wb), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename={}".format("EventData.xlsx")
            return response

        except KeyError as missing_data:
            return JsonResponse({"error_message":"missing credentials in request: {}".format(missing_data)})

        except ContentTypeError:
            return JsonResponse({"error_message":"INVALID TYPE: {}".format(content_type)})

        except InvalidCredentialsError:
            return JsonResponse({"error_message":"Invalid Credentials."})

        except InvalidPermissionsError:
            return JsonResponse({"error_message":"Invalid Permissions"})
