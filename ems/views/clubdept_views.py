from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from events.models import MainEvent
from ems.models.level import LevelClass, LevelInstance
from ems.permissions import IsClubDept
from ems.serializers import *


class ClubDepartmentList(APIView):

	def get():
		pass