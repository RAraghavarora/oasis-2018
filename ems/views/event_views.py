from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import MainEvent
from ems.models.level import LevelClass, LevelInstance


class LevelList(APIView):

	permission_classes = (IsAuthenticated)

	def get(self, request, event_id):
		event = MainEvent.objects.get(pk = event_id)
		levels = LevelClass.objects.filter(event = event)
		serializer = LevelClassSerializer(levels, many = True)
		return Response(serializer.data, status = stauts.HTTP_200_OK)


class LevelDetail(APIView):

	permission_classes = (IsAuthenticated)

	def get(self, request, event_id):
		pass

	def post(self, request, event_id):
		pass

	def delete(self, request, event_id):
		pass