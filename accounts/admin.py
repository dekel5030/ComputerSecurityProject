from django.contrib import admin
from .models import Customer, Password_History

# Register your models here.
admin.site.register(Customer)
admin.site.register(Password_History)