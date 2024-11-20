from django.db import models

# Create your models here.

class Customer(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()