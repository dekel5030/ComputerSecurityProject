import os
from idlelib.query import Query

from django.db import models, connection
from accounts.password_utils import hash, config


class UserManager(models.Manager):
    def create_user(self, username, email, password):
        salt = os.urandom(16)  # Generate salt
        hashed_password = hash(password, salt)  # Hash password
        username = username.lower()
        user = self.create(username=username, email=email, password=hashed_password, salt=salt.hex())
        return user


    def change_password(self, user, new_password):
        salt = os.urandom(16)  # Generate new salt
        hashed_password = hash(new_password, salt)  # Hash new password
        user.password = hashed_password
        user.salt = salt.hex()
        user.save()

    def get_password_history(self):
        return []

    def authenticate(self, username, password):
        user = self.get(username=username)
        if (user.password == hash(password, bytes.fromhex(user.salt))):
            return user
        else:
            return None


class User(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
    salt = models.TextField()

    objects = UserManager()

    def login(self,request):
        request.session['username'] = self.username
        request.session['isLoggedIn'] = True
        print(123)

    def isLoggedIn(self,request):
        if self.username == request.session['username'] and request.session['isLoggedIn'] == True:
            return True
        else:
            return False

    def logout(self,request):
        request.session['isLoggedIn'] = False
        request.session['username'] = None

    def getUser(self, username):
        return User.objects.get(username=username)


class Password_History(models.Model):
    username = models.TextField()
    salt = models.TextField()
    password = models.TextField()
    date_changed = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def addPassword(username, salt, password):
        Password_History.objects.create(username=username, salt=salt, password=password)

    @staticmethod
    def checkPassword(username, password):
        x = Password_History.objects.filter(username=username).order_by('-date_changed')[:config['password_history']]
        for entry in x:
            if hash(password, bytes.fromhex(entry.salt)) == entry.password:
                print("not ok")
                return 0

        print("ok")
        return 1




class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=10,primary_key=True)
    phone_number = models.CharField(max_length=11)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    package = models.CharField(max_length=50)

    @staticmethod
    def add(first_name, last_name, id_number, phone_number, city, email, package):
        if Customer.objects.filter(id_number=id_number).exists():
            print(f"Customer with ID {id_number} already exists.")
            return False
        else:
            Customer.objects.create(first_name=first_name,last_name=last_name,id_number=id_number,
                                    phone_number=phone_number,city=city,email=email,
                                    package=package)
            return True


    def __str__(self):
        return self.first_name

