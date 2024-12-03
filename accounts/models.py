import os;
from django.db import models
from accounts.password_utils import hash

class UserManager(models.Manager):
    def create_user(self, username, email, password):
        salt = os.urandom(16)  # Generate salt
        hashed_password = hash(password, salt)  # Hash password
        user = self.create(username=username, email=email, password=hashed_password, salt=salt.hex())
        return user

    def reset_user_password(self, user, new_password):
        salt = os.urandom(16)  # Generate new salt
        hashed_password = hash(new_password, salt)  # Hash new password
        user.password = hashed_password
        user.salt = salt
        user.save()


class Customer(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
    salt = models.TextField()

class User(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
    salt = models.TextField()

    objects = UserManager()

class Password_History(models.Model):
    username = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="password_history")
    password = models.TextField()
    date_changed = models.DateTimeField(auto_now_add=True)
