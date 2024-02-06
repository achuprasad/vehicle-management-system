from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from .models import UserProfile, UserRole, Vehicle, UserGroup
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm, VehicleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin



class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration_form.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')  
        else:
            return render(request, 'registration_form.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login_form.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vehicle_list')
            else:
                return render(request, 'login_form.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'login_form.html', {'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')



class VehicleListView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        user_group = request.user.userprofile.group
        if user_group:
            if user_group.role == UserRole.SUPER_ADMIN:  
                vehicles = Vehicle.objects.all()
            elif user_group.role == UserRole.ADMIN:  
                vehicles = Vehicle.objects.all()
            elif user_group.role == UserRole.USER:
                vehicles = Vehicle.objects.filter() 
            else:
                vehicles = Vehicle.objects.none()  
        else:
            vehicles = Vehicle.objects.none()  
        return render(request, 'vehicle_list.html', {'vehicles': vehicles})


class VehicleDetailView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        user_group = request.user.userprofile.group
        if user_group and (user_group.role == UserRole.SUPER_ADMIN or user_group.role == UserRole.ADMIN):
            return render(request, 'vehicle_detail.html', {'vehicle': vehicle})
        else:
            return render(request, 'permission_denied.html')

class VehicleCreateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        user_group = request.user.userprofile.group
        if user_group and user_group.role == UserRole.SUPER_ADMIN: 
            form = VehicleForm()
            return render(request, 'vehicle_form.html', {'form': form})
        else:
            return render(request, 'permission_denied.html')

    def post(self, request):
        user_group = request.user.userprofile.group
        if user_group and user_group.role == UserRole.SUPER_ADMIN:  # 
            form = VehicleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('vehicle_list')
            return render(request, 'vehicle_form.html', {'form': form})
        else:
            return render(request, 'permission_denied.html')

class VehicleUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        user_group = request.user.userprofile.group
        print('----user_group-----',user_group)
        if user_group and (user_group.role == UserRole.SUPER_ADMIN or user_group.role == UserRole.ADMIN):
            form = VehicleForm(instance=vehicle)
            return render(request, 'vehicle_form.html', {'form': form, 'vehicle': vehicle})
        else:
            return render(request, 'permission_denied.html')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        user_group = request.user.userprofile.group
        if user_group and (user_group.role == UserRole.SUPER_ADMIN or user_group.role == UserRole.ADMIN):  
            form = VehicleForm(request.POST, instance=vehicle)
            if form.is_valid():
                form.save()
                return redirect('vehicle_list')
            return render(request, 'vehicle_form.html', {'form': form, 'vehicle': vehicle})
        else:
            return render(request, 'permission_denied.html')

class VehicleDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        user_group = request.user.userprofile.group
        if user_group and (user_group.role == UserRole.SUPER_ADMIN or user_group.role == UserRole.ADMIN):
            return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})
        else:
            return render(request, 'permission_denied.html')

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        user_group = request.user.userprofile.group
        if user_group and (user_group.role == UserRole.SUPER_ADMIN or user_group.role == UserRole.ADMIN):
            vehicle.delete()
            return redirect('vehicle_list')
        else:
            return render(request, 'permission_denied.html')
        



class UserProfileCreateView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return render(request, 'permission_denied.html')  
        form = UserProfileForm()
        return render(request, 'user_profile_form.html', {'form': form})

    def post(self, request):
        if not request.user.is_superuser:
            return render(request, 'permission_denied.html')  
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user, created = User.objects.get_or_create(username=username)
            group_name = form.cleaned_data['group_name']
            group, created = UserGroup.objects.get_or_create(name=group_name)
            user_profile = UserProfile.objects.create(user=user, group=group)
            return redirect('/')  
        else:
            return render(request, 'user_profile_form.html', {'form': form})
