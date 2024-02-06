# models.py
from django.db import models
from django.contrib.auth.models import User, Group, Permission

class UserRole:
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    USER = 'user'

    CHOICES = (
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Two', 'Two Wheeler'),
        ('Three', 'Three Wheeler'),
        ('Four', 'Four Wheeler'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    vehicle_model = models.CharField(max_length=50)
    vehicle_description = models.TextField()

    def __str__(self):
        return self.vehicle_number

class UserGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=UserRole.CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=self.name)
        if created:
            if self.role == UserRole.SUPER_ADMIN:
                group.permissions.set(Permission.objects.all())
            elif self.role == UserRole.ADMIN:
                group.permissions.set(Permission.objects.filter(codename__in=['view_vehicle', 'change_vehicle']))
            elif self.role == UserRole.USER:
                group.permissions.set(Permission.objects.filter(codename='view_vehicle'))
            else:
                raise ValueError("Invalid role")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
