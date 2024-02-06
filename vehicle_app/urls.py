from django.urls import path
from . import views
urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('create_profile/', views.UserProfileCreateView.as_view(), name='create_profile'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]