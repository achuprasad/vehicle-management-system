from django.shortcuts import render
from django.views import View
from django.http import HttpResponseForbidden

from vehicle_app.models import UserRole

def custom_decorator(func):
    """
    Custom decorator to restrict access to a class-based view.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, 'permission_denied.html')  
        return func(request, *args, **kwargs)
    return wrapper


def custom_decorator_admin(func):
    """
    Custom decorator to restrict access to a class-based view.
    """
    def wrapper(request, *args, **kwargs):
        user_group = request.user.userprofile.group
        if not (user_group == UserRole.SUPER_ADMIN or user_group == UserRole.ADMIN):
            return render(request, 'permission_denied.html')  
        return func(request, *args, **kwargs)
    return wrapper