from django.db import models

# Create your models here.

class Customer(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()

class Password_History(models.Model):
    username = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="password_history")
    password = models.TextField()
    date_changed = models.DateTimeField(auto_now_add=True)
