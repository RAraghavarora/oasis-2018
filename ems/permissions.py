from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from ems.models.clubdept import ClubDepartment

class IsClubDept(BasePermission):

	def has_permission(self, request, view):
		user = request.user
		is_superuser = user.is_superuser
		is_club_dept = ClubDepartment.objects.filter(user = user).exists()
		
		return is_superuser or is_club_dept


class IsActiveJudge(BasePermission):

	def has_permission(self, request, view):
		user = request.user
		judge = Judge.objects.filter(user = user)
		
		return judge.exists() and judge[0].is_active

class IsControls(BasePermission):
	
	def has_permission(self, request, view):
		user = request.user
		return user.is_superuser or user.username == 'controls'