from rest_framework import serializers

from events.models import Category, MainProfShow

class CategorySerializer(serializers.ModelSerializer):
	events = serializers.SerializerMethodField()

	def get_events(self, obj):
		print("GET EVENTS")
		events = obj.mainevent_set.all()
		data = {}
		for event in events:
			data[event.name] = event.content
		return data

	class Meta:
		model = Category
		fields = ('name', 'events',)


class MainProfShowSerializer(serializers.ModelSerializer):

	class Meta:
		model = MainProfShow
		fields = '__all__'
