from django.contrib import admin

from .models import Vehicle,UserProfile,UserGroup


# Register your models here.
admin.site.register(Vehicle)
admin.site.register(UserProfile)
admin.site.register(UserGroup)