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
    path('dashboard/<consoleName>/order/details/<int:orderId>/',views.orderDetails,name='orderDetails'),
    path('dashboard/<consoleName>/order/details/update/delivery/date/',views.orderUpdateDDate,name='orderUpdateDDate'),
    path('dashboard/<consoleName>/order/details/update/delivery/date/eng/',views.enorderUpdateDDate,name='enorderUpdateDDate'),
    path('dashboard/<consoleName>/order/comment/',views.newComment,name='newComment'),
    path('dashboard/<consoleName>/manage/inventory/',views.manageInventory,name='manageInventory'),


    path('dashboard/<consoleName>/order/dispatch/<int:orderId>/',views.orderDispatch,name='orderDispatch'),
    path('dashboard/<consoleName>/order/provisionally/schedule/<int:orderId>/',views.orderSchedule,name='orderSchedule'),
    path('dashboard/<consoleName>/provisional/schedule/',views.provisionalSchedule,name='provisionalSchedule'),

    path('dashboard/<consoleName>/provisional/schedule/delete/',views.deleteProvisionalSchedule,name='deleteProvisionalSchedule'),
    path('dashboard/<consoleName>/provisional/schedule/update/',views.updateProvisionalSchedule,name='updateProvisionalSchedule'),

    path('dashboard/<consoleName>/provisional/schedule/final/',views.finalProvisionalSchedule,name='finalProvisionalSchedule'),

    path('dashboard/<consoleName>/order/history/',views.orderHistory,name='orderHistory'),
    
    path('export/order/history/',views.exportOrderHistory,name='exportOrderHistory'),

    path('dashboard/<consoleName>/order/cancel/',views.orderCancel,name='orderCancel'),
    path('dashboard/<consoleName>/order/update/payment/status/',views.orderUpdatePaymentStatus,name='orderUpdatePaymentStatus'),
    path('dashboard/<consoleName>/order/update/order/type/',views.orderUpdateType,name='orderUpdateType'),
    # For Order File Upload
    path('dashboard/<consoleName>/order/upload/',views.orderUpload,name='orderUpload'),
    path('dashboard/<consoleName>/invoice/upload/',views.invoiceUpload,name='invoiceUpload'),

     # For Warehouse Console
    path('dashboard/<consoleName>/inventory/details/',views.warehouseInventory,name='warehouseInventory'),
    path('dashboard/<consoleName>/inventory/dashboard/',views.warehouseInventoryDashboard,name='warehouseInventoryDashboard'),
    path('dashboard/<consoleName>/inventory/requirement/',views.stockRequirement,name='stockRequirement'),
    path('dashboard/<consoleName>/inventory/requirement/delete/<int:id>/',views.stockRequirementDelete,name='stockRequirementDelete'),
    path('dashboard/<consoleName>/inventory/requirement/details/<int:id>/',views.stockRequirementDetails,name='stockRequirementDetails'),
    path('dashboard/<consoleName>/update/inventory/requirement/',views.updateStockRequirement,name='updateStockRequirement'),
    path('dashboard/<consoleName>/upload/stock/requirement/recieved/',views.uploadStockRequirement,name='uploadStockRequirement'),
    path('dashboard/<consoleName>/inventory/upload/',views.warehouseInventoryUpload,name='warehouseInventoryUpload'),
    path('export/excel/inventory/', views.exportInventoryExcel,name='exportInventoryExcel'),
    path('export/excel/stock/', views.exportStockExcel,name='exportStockExcel'),


    # For Buffing Department
    path('dashboard/<consoleName>/order/buv87u/',views.buffingOrders,name='buffingOrders'),
    path('dashboard/<consoleName>/order/buv87u/complete/',views.completeBuffingOrders,name='completeBuffingOrders'),

    # For Plating Department
    path('dashboard/<consoleName>/order/buv835ww2w37u/',views.platingOrders,name='platingOrders'),
    path('dashboard/<consoleName>/order/buv87412u/complete/',views.completePlatingOrders,name='completePlatingOrders'),


    # For 4S Buffing Department
    path('dashboard/<consoleName>/order/buffing4s/',views.sBuffingOrders,name='sBuffingOrders'),
    path('dashboard/<consoleName>/order/buv84sbuff/complete/',views.complete4SBuffingOrders,name='complete4SBuffingOrders'),


    # For Laquer Department
    path('dashboard/<consoleName>/order/slsaquedasrj23j/',views.laquerOrders,name='laquerOrders'),
    path('dashboard/<consoleName>/order/buv84slaq/complete/',views.completeLaquerOrders,name='completeLaquerOrders'),


    # For Engineering Department
    path('dashboard/<consoleName>/order/slsaqeng/',views.engineeringOrders,name='engineeringOrders'),
    path('dashboard/<consoleName>/order/buv84engaq/complete/',views.completeEngineeringOrders,name='completeEngineeringOrders'),

    # For Packaging Department
    path('dashboard/<consoleName>/order/pack/',views.packagingOrders,name='packagingOrders'),
    path('dashboard/<consoleName>/order/pack/complete/',views.completePackagingOrders,name='completePackagingOrders'),


    path('dashboard/<consoleName>/order/warehouse/decww3kk3/',views.warehouseOrders,name='warehouseOrders'),

    path('dashboard/<consoleName>/complete/order/warehouse/decww3kk3/',views.completeWarehouseOrders,name='completeWarehouseOrders'),



    
] 