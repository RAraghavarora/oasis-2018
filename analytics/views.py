import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from analytics.models import Video, ViewTimer

@csrf_exempt
def views(request, name=None):
    if request.method == "GET":
        if(name):
            try:
                video = Video.objects.get(name=name.replace("+", " "))
            except Exception as error:
                return JsonResponse({"message": "no such video exists. {}.".format(error)}, status=400)
            return JsonResponse({
                "name":video.name,
                "views":video.views
            })
        else:
            return JsonResponse([{"name":video.name, "views":video.views} for video in Video.objects.all()], safe=False)

    elif request.method == "POST":
        if not name:
            # 1 - Ensure compatibility for JSON and Form Encoded Data
            try:
                if request.META["CONTENT_TYPE"] == "application/json":
                    data = json.loads(request.body.decode('utf-8'))
                else:
                    data = request.POST
            except:
                data = request.POST
            # /1
            try:
                name = data["name"]
            except KeyError as field:
                return JsonResponse({"message": "missing value for key: {}.".format(field)}, status=400)
            try:
                video = Video.objects.get(name=name.replace("+", " "))
            except Exception as error:
                return JsonResponse({"message": "no such video exists. {}.".format(error)}, status=400)
            video.incrementViews()
            return JsonResponse({"name":video.name ,"views":video.views})
        else:
            return JsonResponse({"message":"Invalid URL pattern -- Don't specify a video in the URL."}, status=400)

    else:
        return JsonResponse({"message":"Invalid method."}, status=405)

@csrf_exempt
def viewTime(request):
    if request.method == "GET":
        return JsonResponse([{"date":viewtimer.date, "time":viewtimer.time, "seconds_viewed":viewtimer.seconds_viewed} for viewtimer in ViewTimer.objects.all()], safe=False)

    if request.method == "POST":
        # 1 - Ensure compatibility for JSON and Form Encoded Data
        try:
            if request.META["CONTENT_TYPE"] == "application/json":
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST
        except:
            data = request.POST
        # /1
        try:
            time = data["seconds_viewed"]
            viewtimer = ViewTimer.objects.create(seconds_viewed=time)
            return JsonResponse({"date":viewtimer.date, "time":viewtimer.time, "seconds_viewed":viewtimer.seconds_viewed})
        except ValueError:
            return JsonResponse({"message": "invalid type for key: seconds_viewed. Must be int."}, status=400)
        except KeyError as field:
            return JsonResponse({"message": "missing value for key: {}.".format(field)}, status=400)

    else:
        return JsonResponse({"message":"Invalid method."}, status=405)
