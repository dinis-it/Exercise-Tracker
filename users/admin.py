from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(BaseUser, UserAdmin)
admin.site.register(Profile)
admin.site.register(Weight)
