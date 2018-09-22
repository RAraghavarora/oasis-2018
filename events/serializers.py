from rest_framework import serializers

from events.models import Category

class CategorySerializer(serializers.ModelSerializer):
	events = serializers.SerializerMethodField()

	def get_events(self, obj):
		print("GET EVENTS")
		events = obj.mainevent_set.all()
		print(events)
		data = {}
		for event in events:
			data[event.name] = event.content
		print(data)
		return data

	class Meta:
		model = Category
		fields = ('name', 'events',)