from django.urls import path
from mainApp import views
urlpatterns = [
    path('',views.handleLogin,name='login'),
    path('logout/',views.handle_logout,name='logout'),
    path('consoles/',views.consoles,name='consoles'),
    path('dashboard/<consoleName>/',views.dashboard,name='dashboard'),
    # For new Employee registration
    path('dashboard/<consoleName>/register/employee/',views.registerEmployee,name='registerEmployee')
]