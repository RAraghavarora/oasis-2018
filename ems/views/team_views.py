from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TeamList(APIView):

	permission_classes = (IsAuthenticated)

	def get(self, request):
		pass

	def post(self, request):
		pass

class TeamDetail(APIView):

	permission_classes = (IsAuthenticated)

	def get(self, request, team_id):
		pass

	def post(self, request, team_id):
		pass

	def delete(self, request, team_id):
		pass