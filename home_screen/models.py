
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=10,primary_key=True)
    phone_number = models.CharField(max_length=11)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    package = models.CharField(max_length=50)


    def __str__(self):
        return self.name

