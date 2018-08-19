import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from analytics.models import Video

@csrf_exempt
def views(request, name=None):
    if request.method == "GET":
        if(name):
            video = get_object_or_404(Video, name=name.replace("+", " "))
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
            video = get_object_or_404(Video, name=data["name"].replace("+", " "))
            video.incrementViews()
            return JsonResponse({"name":video.name ,"views":video.views})
        else:
            return JsonResponse({"message":"Invalid URL pattern -- Don't specify a video in the URL."}, status=400)

    else:
        return JsonResponse({"message":"Invalid method."}, status=405)
