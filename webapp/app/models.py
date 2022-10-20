from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Service(models.Model):
	title = models.TextField()
	price = models.IntegerField()


class Appointment(models.Model):
	user_id = models.IntegerField()
	services = ArrayField(models.IntegerField())
	date = models.DateField()
	time = models.TimeField()