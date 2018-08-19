from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=100, unique=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def incrementViews(self):
        self.views += 1
        self.save()
