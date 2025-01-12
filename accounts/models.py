import os

from django.db import models, connection
from accounts.password_utils import hash, config


class UserManager(models.Manager):
    def create_user(self, username, email, password):
        salt = os.urandom(16)  # Generate salt
        hashed_password = hash(password, salt)  # Hash password
        username = username.lower()
        raw_query = f"""
    INSERT INTO accounts_user (username, email, password,salt) 
    VALUES ('{username}', '{email}','{hashed_password}','{salt.hex()}');
"""
        # Execute the insert query
        with connection.cursor() as cursor:
            cursor.executescript(raw_query)
        # Fetch the created user
        with connection.cursor() as cursor:
            fetch_query = f"SELECT username, email, password, salt FROM accounts_user WHERE username = '{username}'"
            cursor.executescript(fetch_query)
            user_data = cursor.fetchone()
        # Map the fetched data to a User instance or return None
        if user_data:
            return User(username=user_data[0], email=user_data[1], password=user_data[2], salt=user_data[3])
        return None


    def change_password(self, user, new_password):
        salt = os.urandom(16)  # Generate new salt
        hashed_password = hash(new_password, salt)  # Hash new password
        user.password = hashed_password
        user.salt = salt.hex()
        user.save()

    def get_password_history(self):
        return []


    def authenticate(self,username,password):
        #user = self.get(username=username)
        # You can use sql injection to bypass password requirements.
        # ' OR 1=1;---
        username = username.lower()
        Query = f"SELECT salt FROM accounts_User where username = '{username}';"

        # Fetch the user
        with connection.cursor() as cursor:
            cursor.execute(Query)
            user_data = cursor.fetchone()
        if user_data:
            # Map fetched data to a dictionary or a model-like structure
            Query = f"SELECT username, email, password, salt FROM accounts_User where username = '{username}' AND password = '{hash(password, bytes.fromhex(user_data[0]))}';"
            with connection.cursor() as cursor:
                cursor.execute(Query)
                user_data = cursor.fetchone()
            if not user_data:
                return None
            # user =  {
            #     "username": user_data[0],
            #     "email": user_data[1],
            #     "password": user_data[2],
            #     "salt": user_data[3],
            # }
            # if (user["password"] == hash(password, bytes.fromhex(user["salt"]))):
            return User(username=user_data[0], email=user_data[1], password=user_data[2], salt=user_data[3])
            # else:
                # return None
        else:
            return None
# dekel - 12345678aB
# NotMe - 2345678Ab

class User(models.Model):
    username = models.TextField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
    salt = models.TextField()

    objects = UserManager()

    def login(self,request):
        request.session['username'] = self.username
        request.session['isLoggedIn'] = True

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
            raw_query = f"""
                            INSERT INTO accounts_Customer (first_name, last_name, id_number, phone_number, city, email, package)
                            VALUES ('{first_name}', '{last_name}', '{id_number}', '{phone_number}', '{city}', '{email}', '{package}');
                         """
            with connection.cursor() as cursor:
                cursor.executescript(raw_query)

            return True


    def __str__(self):
        return self.first_name
