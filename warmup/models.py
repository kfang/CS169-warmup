from django.db import models

class User(models.Model):
	name		= models.CharField(max_length=128, primary_key = True)
	password	= models.CharField(max_length=128)
	num_logins	= models.PositiveIntegerField()

# Create your models here.
