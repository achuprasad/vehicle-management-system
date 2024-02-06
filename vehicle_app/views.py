from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Vehicle
from .forms import VehicleForm
# Create your views here.




@method_decorator(login_required, name='dispatch')
class VehicleListView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        return render(request, 'vehicle_list.html', {'vehicles': vehicles})
    


@method_decorator(login_required, name='dispatch')
class VehicleDetailView(View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        return render(request, 'vehicle_detail.html', {'vehicle': vehicle})
    

@method_decorator(login_required, name='dispatch')
class VehicleCreateView(View):
    def get(self, request):
        form = VehicleForm()
        return render(request, 'vehicle_form.html', {'form': form})

    def post(self, request):
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
        return render(request, 'vehicle_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class VehicleUpdateView(View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(instance=vehicle)
        return render(request, 'vehicle_form.html', {'form': form, 'vehicle': vehicle})

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
        return render(request, 'vehicle_form.html', {'form': form, 'vehicle': vehicle})

@method_decorator(login_required, name='dispatch')
class VehicleDeleteView(View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})

    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return redirect('vehicle_list')
