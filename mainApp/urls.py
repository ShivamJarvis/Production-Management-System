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
    # For Add Supplier

    path('dashboard/<consoleName>/supplier/add/',views.addSupplier,name='addSupplier'),
    path('dashboard/<consoleName>/supplier/list/',views.listSupplier,name='listSupplier'),

    # For Production Console
    path('dashboard/<consoleName>/order/summary/',views.orderSummary,name='orderSummary'),


    path('dashboard/<consoleName>/order/dispatch/<int:orderId>/',views.orderDispatch,name='orderDispatch'),
    path('dashboard/<consoleName>/provisional/schedule/',views.provisionalSchedule,name='provisionalSchedule'),
    path('dashboard/<consoleName>/order/history/',views.orderHistory,name='orderHistory'),
    path('dashboard/<consoleName>/order/cancel/',views.orderCancel,name='orderCancel'),
    path('dashboard/<consoleName>/order/update/payment/status/',views.orderUpdatePaymentStatus,name='orderUpdatePaymentStatus'),
    # For Order File Upload
    path('dashboard/<consoleName>/order/upload/',views.orderUpload,name='orderUpload'),

     # For Warehouse Console
    path('dashboard/<consoleName>/inventory/details/',views.warehouseInventory,name='warehouseInventory'),
    path('dashboard/<consoleName>/inventory/requirement/',views.stockRequirement,name='stockRequirement'),
    path('dashboard/<consoleName>/update/inventory/requirement/',views.updateStockRequirement,name='updateStockRequirement'),
    path('dashboard/<consoleName>/upload/stock/requirement/recieved/',views.uploadStockRequirement,name='uploadStockRequirement'),
    path('dashboard/<consoleName>/inventory/upload/',views.warehouseInventoryUpload,name='warehouseInventoryUpload'),
    path('export/excel/inventory/', views.exportInventoryExcel,name='exportInventoryExcel'),
    path('export/excel/stock/', views.exportStockExcel,name='exportStockExcel'),
] 