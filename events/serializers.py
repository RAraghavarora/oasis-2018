from rest_framework import serializers

from events.models import Category, MainProfShow, MainEvent


class CategorySerializer(serializers.ModelSerializer):
	events = serializers.SerializerMethodField()

	def get_events(self, obj):
		events = obj.mainevent_set.all()
		data = {}
		for event in events:
			data[event.name] = event.content
			data[event.detail_rules]=event.detail_rules
		return data

	class Meta:
		model = Category
		fields = ('name', 'events',)


class MainProfShowSerializer(serializers.ModelSerializer):

	class Meta:
		model = MainProfShow
		fields = '__all__'


class MainEventSerializer(serializers.ModelSerializer):
	category = serializers.SerializerMethodField()

	def get_category(self, obj):
		return obj.category.name

	class Meta:
		model = MainEvent
		fields = ('id', 'name', 'content', 'appcontent', 'short_description', 'date', 'time', 'category', 'duration', 'rules', 'venue')
