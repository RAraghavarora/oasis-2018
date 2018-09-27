from rest_framework import serializers

from ems.models.clubdept import ClubDepartment
from ems.models.judge import Judge
from ems.models.level import LevelClass, LevelInstance
from ems.models.parameter import ParameterClass, ParameterInstance
from ems.models.team import Team


class ClubDeptSerializer(serializers.ModelSerializer):

	class Meta:
		model = ClubDepartment
		fields = '__all__'


class JudgeSerializer(serializers.ModelSerializer):

	class Meta:
		model = Judge
		fields = '__all__'


class LevelClassSerializer(serializers.ModelSerializer):

	class Meta:
		model = LevelClass
		fields = '__all__'


class LevelInstanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = LevelInstance
		fields = '__all__'


class ParameterClassSerializer(serializers.ModelSerializer):

	class Meta:
		model = ParameterClass
		fields = '__all__'


class ParameterInstanceSerializer(serializers.ModelSerializer):

	class Meta:
		model = ParameterInstance
		fields = '__all__'



class TeamSerializer(serializers.ModelSerializer):

	class Meta:
		model = Team
		fields = '__all__'
