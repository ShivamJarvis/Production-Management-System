from django.urls import path
from mainApp import views
urlpatterns = [
    path('',views.handleLogin,name='login'),
    path('logout/',views.handle_logout,name='logout'),
    path('consoles/',views.consoles,name='consoles'),
    path('dashboard/<consoleName>/',views.dashboard,name='dashboard'),
    # For new Employee registration
    path('dashboard/<consoleName>/register/employee/',views.registerEmployee,name='registerEmployee'),
    # For changing permission and set employee to active/inactive
    path('dashboard/<consoleName>/see/employee/details/',views.employeeDetails,name='employeeDetails'),
    # For changing permission and set employee to active/inactive With DepartmentName Filter
    path('dashboard/<consoleName>/see/employee/details/filteron/',views.employeeDetailsWithFilter,name='employeeDetailsWithFilter'),
    # For Activate the User/Employee
    path('dashboard/<consoleName>/activate/employee/<int:empId>/',views.activateEmployeeDetails,name='activateEmployeeDetails'),
    # For Inactivate the User/Employee
    path('dashboard/<consoleName>/inactivate/employee/<int:empId>/',views.inActivateEmployeeDetails,name='inActivateEmployeeDetails'),
    # For Change the User/Employee Permission
    path('dashboard/<consoleName>/employee/<int:empId>/permissions/',views.employeePermissions,name='employeePermissions'),

    # For Production Console
    path('dashboard/<consoleName>/order/summary/',views.orderSummary,name='orderSummary'),
    path('dashboard/<consoleName>/provisional/schedule/',views.provisionalSchedule,name='provisionalSchedule'),
    path('dashboard/<consoleName>/order/history/',views.orderHistory,name='orderHistory'),



]