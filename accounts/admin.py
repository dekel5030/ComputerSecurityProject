from django.contrib import admin
from .models import User, Password_History

# Register your models here.
admin.site.register(User)
admin.site.register(Password_History)