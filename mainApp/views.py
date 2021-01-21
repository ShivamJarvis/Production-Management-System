from io import BytesIO, StringIO
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from numpy.core.numeric import NaN
from pandas import io
from pandas.io import excel
from mainApp import models
from mainApp.models import Inventory, Order, Supplier, UserData, StockRequirement
import pandas as pd
import xlwt
import xlsxwriter
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import Permission, User
from datetime import datetime
# Create your views here.
def handleLogin(request):
    if request.user.username:
        return redirect('consoles')
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']
        if not loginUsername == "":
            if not loginPassword == "":
                userAuthentication = authenticate(username=loginUsername,password=loginPassword)
                if userAuthentication:
                    login(request,userAuthentication)
                    return redirect('consoles')
                else:
                    pass
            else:
                pass
        else:
            pass
    return render(request,'pms/login.html')

@login_required(login_url='login')
def handle_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def consoles(request):
    userAccessPermissions = UserData.objects.filter(user=request.user).all()
    production = False
    warehouse = False
    plating = False
    buffing = False
    sBuffing = False
    packaging = False
    laquer = False
    engineering = False

    for userAccessPermission in userAccessPermissions:
        if(userAccessPermission.permission == 'Production'):
            production = True
        elif(userAccessPermission.permission == 'Warehouse'):
            warehouse = True
        elif(userAccessPermission.permission == 'Plating'):
            plating = True
        elif(userAccessPermission.permission == 'Buffing'):
            buffing = True
        elif(userAccessPermission.permission == '4S Buffing'):
            sBuffing = True
        elif(userAccessPermission.permission == 'Packaging'):
            packaging = True
        elif(userAccessPermission.permission == 'Laquer'):
            laquer = True
        elif(userAccessPermission.permission == 'Engineering'):
            engineering = True
    
    context = {
        'production':production,
        'warehouse':warehouse,
        'plating':plating,
        'buffing':buffing,
        'sbuffing':sBuffing,
        'packaging':packaging,
        'laquer':laquer,
        'engineering':engineering
    }


    return render(request,'pms/consoles.html',context)

@login_required(login_url='login')
def dashboard(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    context = {
        'consoleName':consoleName
    }
    return render(request,'pms/dashboard_base.html',context)

@login_required(login_url='login')
def registerEmployee(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    if(not request.user.is_superuser):
        return redirect('consoles')
    if(request.method == 'POST'):
        password = request.POST['password']
        rePassword = request.POST['repassword']
        if password == rePassword:
            firstName = request.POST['fname']
            lastName = request.POST['lname']
            userName = request.POST['username']
            userType = request.POST['usertype']
            production = request.POST.get('production')
            warehouse = request.POST.get('warehouse')
            plating = request.POST.get('plating')
            buffing = request.POST.get('buffing')
            sBuffing = request.POST.get('sbuffing')
            packaging = request.POST.get('packaging')
            engineering = request.POST.get('engineering')
            laquer = request.POST.get('laquer')
            active = request.POST.get('active')
            is_active=True
            if active == "active":
                is_active=True
            else:
                is_active = False

            is_admin = False
            is_staff = False
            if not userType == 'user':
                is_admin = True
                is_staff = True
            

            newUser = User.objects.create_user(first_name=firstName,last_name=lastName,username=userName,is_active=is_active,is_staff=is_staff,password=password,is_superuser=is_admin)

            if(production=='production'):
                production_permission = UserData(user=newUser,permission="Production")
                production_permission.save()

            if(warehouse=='warehouse'):
                warehouse_permission = UserData(user=newUser,permission="Warehouse")
                warehouse_permission.save()

            if(plating=='plating'):
                plating_permission = UserData(user=newUser,permission="Plating")
                plating_permission.save()

            if(buffing=='buffing'):
                buffing_permission = UserData(user=newUser,permission="Buffing")
                buffing_permission.save()

            if(sBuffing=='sbuffing'):
                sbuffing_permission = UserData(user=newUser,permission="4S Buffing")
                sbuffing_permission.save()

            if(packaging=='packaging'):
                packaging_permission = UserData(user=newUser,permission="Packaging")
                packaging_permission.save()
                
            if(engineering=='engineering'):
                engineering_permission = UserData(user=newUser,permission="Engineering")
                engineering_permission.save()

            if(laquer=='laquer'):
                laquer_permission = UserData(user=newUser,permission="Laquer")
                laquer_permission.save()



    context = {
        'consoleName':consoleName
    }
    return render(request,'pms/registration.html',context)


@login_required(login_url='login')
def employeeDetails(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    userDetails = User.objects.filter(is_superuser=False).all()
    userDepartmentDetails = UserData.objects.filter(user__is_superuser=False).all()

    context = {
        'userDetails':userDetails,
        'consoleName':consoleName,
        'userDepartmentDetails':userDepartmentDetails
    }
    return render(request,'pms/employee_details.html',context)


@login_required(login_url='login')
def activateEmployeeDetails(request,empId,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    user = User.objects.filter(id=empId).first()
    user.is_active = True
    user.save()
    return redirect('employeeDetails',consoleName=consoleName)


@login_required(login_url='login')
def inActivateEmployeeDetails(request,empId,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    user = User.objects.filter(id=empId).first()
    user.is_active = False
    user.save()
    return redirect('employeeDetails',consoleName=consoleName)


@login_required(login_url='login')
def employeePermissions(request,consoleName,empId):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    userDetails = UserData.objects.filter(user__id=empId).all()
    user = User.objects.filter(id=empId).first()
    userCurrentPermissions = []
    for permission in userDetails:
        userCurrentPermissions.append(permission.permission)
    if request.method == 'POST':
        production = request.POST.get('production')
        warehouse = request.POST.get('warehouse')
        plating = request.POST.get('plating')
        buffing = request.POST.get('buffing')
        sBuffing = request.POST.get('sbuffing')
        packaging = request.POST.get('packaging')
        engineering = request.POST.get('engineering')
        laquer = request.POST.get('laquer')
        try:
            if(production=='production'):
                if('Production' not in userCurrentPermissions):
                    production_permission = UserData(user=user,permission="Production")
                    production_permission.save()
            else:
                production_permission = UserData.objects.filter(permission='Production').filter(user=user).first()
                production_permission.delete()
        except:
            pass

        try:
            if(warehouse=='warehouse'):
                if('Warehouse' not in userCurrentPermissions):
                    warehouse_permission = UserData(user=user,permission="Warehouse")
                    warehouse_permission.save()
            else:
                warehouse_permission = UserData.objects.filter(permission='Warehouse').filter(user=user).first()
                warehouse_permission.delete()
        except:
            pass
        try:
            if(plating=='plating'):
                if('Plating' not in userCurrentPermissions):
                    plating_permission = UserData(user=user,permission="Plating")
                    plating_permission.save()
            else:
                plating_permission = UserData.objects.filter(permission='Plating').filter(user=user).first()
                plating_permission.delete()
        except:
            pass

        try:
            if(buffing=='buffing'):
                if('Buffing' not in userCurrentPermissions):
                    buffing_permission = UserData(user=user,permission="Buffing")
                    buffing_permission.save()
            else:
                buffing_permission = UserData.objects.filter(permission='Buffing').filter(user=user).first()
                buffing_permission.delete()
        except:
            pass

        try:
            if(sBuffing=='sbuffing'):
                if('4S Buffing' not in userCurrentPermissions):
                    sbuffing_permission = UserData(user=user,permission="4S Buffing")
                    sbuffing_permission.save()
            else:
                sbuffing_permission = UserData.objects.filter(permission='4S Buffing').filter(user=user).first()
                sbuffing_permission.delete()
        except:
            pass

        try:
            if(packaging=='packaging'):
                if('Packaging' not in userCurrentPermissions):
                    packaging_permission = UserData(user=user,permission="Packaging")
                    packaging_permission.save()
            else:
                packaging_permission = UserData.objects.filter(permission='Packaging').filter(user=user).first()
                packaging_permission.delete()
        except:
            pass

        try:
            if(engineering=='engineering'):
                if('Engineering' not in userCurrentPermissions):
                    engineering_permission = UserData(user=user,permission="Engineering")
                    engineering_permission.save()
            else:
                engineering_permission = UserData.objects.filter(permission='Engineering').filter(user=user).first()
                engineering_permission.delete()
        except:
            pass
        try:
            if(laquer=='laquer'):
                if('Laquer' not in userCurrentPermissions):
                    laquer_permission = UserData(user=user,permission="Laquer")
                    laquer_permission.save()
            else:
                laquer_permission = UserData.objects.filter(permission='Laquer').filter(user=user).first()
                laquer_permission.delete()
        except:
            pass

        return redirect('employeePermissions',consoleName=consoleName,empId=empId)

    context = {
        'consoleName':consoleName,
        'empId':empId,
        'userCurrentPermissions':userCurrentPermissions,
        'user':user
    }
    return render(request,'pms/employee_permission.html',context)


@login_required(login_url='login')
def employeeDetailsWithFilter(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    userInDepartment = []
    filteredDepartmentName = ''
    if(request.method=='POST'):
        filteredDepartmentName = request.POST['departmentName']
        fromDate = request.POST['from']
        toDate = request.POST['to']
        try:
            
            fromDate = datetime.strptime(fromDate, '%Y-%m-%d').date()
            toDate = datetime.strptime(toDate, '%Y-%m-%d').date()
        except:
            pass
        if not filteredDepartmentName == 'All':
            try:
                departmentNameFilter = User.objects.filter(date_joined__range=[fromDate,toDate]).all()
            except:
                departmentNameFilter = User.objects.all()

            for user in departmentNameFilter:
                userData = UserData.objects.filter(user=user).filter(permission=filteredDepartmentName).first()
                if userData:
                    userInDepartment.append(userData.user)
           
        else:
            try:
                userInDepartment = User.objects.filter(is_superuser=False).filter(date_joined__range=[fromDate,toDate]).all()
            except:
                userInDepartment = User.objects.filter(is_superuser=False).all()

            userInDepartment = list(userInDepartment)
            
            
    

    context = {
        'consoleName' : consoleName,
        'departmentName':filteredDepartmentName,
        'userDetails':userInDepartment
    }
    return render(request,'pms/employee_details.html',context)

@login_required(login_url='login')
def orderSummary(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    
    orderData = Order.objects.all()

    context = {
        'consoleName':consoleName,
        'orderData':orderData
    }
    return render(request,'pms/order_summary.html',context)


@login_required(login_url='login')
def provisionalSchedule(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    context = {
        'consoleName':consoleName
    }
    return render(request,'pms/provisional_schedule.html',context)



@login_required(login_url='login')
def orderHistory(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    context = {
        'consoleName':consoleName
    }
    return render(request,'pms/order_history.html',context)


@login_required(login_url='login')
def orderUpload(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    if request.method == 'POST':
        orderFile = request.FILES['order_file']
        fs = FileSystemStorage()
        filename = fs.save(orderFile.name,orderFile)        
        if orderFile:
            data = pd.read_excel('media/'+orderFile.name,engine='openpyxl')
            data['Direct Orders'] = data['Direct Orders'].fillna('Others')
            lenOfData = len(data)
            for i in range(0,lenOfData):
                orderType = data['Direct Orders'][i]
                salesOrderNo = data['Sales Order'][i]
                customerName = data['Customer'][i]
                orderDate = data['Date'][i]
                description = data['Description'][i]
                itemCode = data['Item'][i]
                deliveryDate = data['Item Delivery Date'][i]
                orderQuantity = data['Qty'][i]
                newOrder = Order(order_type=orderType,sales_order=salesOrderNo,customer_name=customerName,order_date=orderDate,item_code=itemCode,item_delivery_date=deliveryDate,order_qty=orderQuantity,description=description,status='Pending')
                newOrder.save()
        
                inventory = Inventory.objects.filter(item_code = itemCode).first()
                if inventory:
                    requiredQty = inventory.balanced_qty - orderQuantity
                    if requiredQty<0:
                        stockRequirement = StockRequirement.objects.filter(order__item_code=itemCode).first()
                        if stockRequirement:
                            newStockRequirement = StockRequirement(order=newOrder,required_qty= orderQuantity, pending_qty = orderQuantity,recieved_qty=0)
                            newStockRequirement.save()
                        else:
                            requiredQty = (inventory.balanced_qty - orderQuantity) * (-1)
                            newStockRequirement = StockRequirement(order=newOrder,required_qty= requiredQty, pending_qty = requiredQty,recieved_qty=0)
                            newStockRequirement.save()
                else:
                    inventory = Inventory(item_code=itemCode,opening_qty=0,added_qty=0,issued_dispatched_qty=0,balanced_qty=0)
                    inventory.save()
                    newStockRequirement = StockRequirement(order=newOrder,required_qty= orderQuantity, pending_qty = orderQuantity,recieved_qty=0)
                    newStockRequirement.save()
    return redirect('orderSummary',consoleName)


@login_required(login_url='login')
def warehouseInventory(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    inventoryData = Inventory.objects.all()
    context = {
        'consoleName':consoleName,
        'inventoryData':inventoryData
    }
    return render(request,'pms/warehouse_inventory.html',context)

@login_required(login_url='login')
def warehouseInventoryUpload(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    if request.method == 'POST':
        inventoryFile = request.FILES['inventory_file']
        fs = FileSystemStorage()
        filename = fs.save(inventoryFile.name,inventoryFile)
        if inventoryFile:
            data = pd.read_excel('media/'+inventoryFile.name,engine='openpyxl')
            data['Opening Quantity'] = data['Opening Quantity'].fillna(0)
            data['Added Quantity'] = data['Added Quantity'].fillna(0)
            data['Issued / Dispatched'] = data['Issued / Dispatched'].fillna(0)
            data['Balance Quantity'] = data['Balance Quantity'].fillna(0)
            lenOfData = len(data)
            for i in range(0,lenOfData):
                try:
                    itemCode = data['Item'][i]
                    openingQty = data['Opening Quantity'][i]
                    addedQty = data['Added Quantity'][i]
                    issuedQty = data['Issued / Dispatched'][i]
                    balanceQty = data['Balance Quantity'][i]
                    item = Inventory(item_code=itemCode,opening_qty=openingQty,added_qty=addedQty,issued_dispatched_qty=issuedQty,balanced_qty=balanceQty)
                    item.save()
                except:
                    itemCode = data['Item'][i]
                    print(itemCode)
    context = {
        'consoleName':consoleName
    }
    return redirect('warehouseInventory',consoleName)

@login_required(login_url='login')
def exportInventoryExcel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    format = workbook.add_format({'num_format': 'dd/mm/yy'})
    worksheet.write('A1','Item')
    worksheet.write('B1','Opening Quantity')
    worksheet.write('C1','Added Quantity')
    worksheet.write('D1','Issued / Dispatched')
    worksheet.write('E1','Balance Quantity')
    allData = Inventory.objects.all().values_list('item_code','opening_qty','added_qty','issued_dispatched_qty','balanced_qty')
    col = ['A','B','C','D','E']
    row_num=1
    for data in allData:
        row_num += 1
        for col_num in range(len(data)):
            worksheet.write(str(col[col_num]+str(row_num)),data[col_num],format)
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="inventory.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response
    
@login_required(login_url='login')
def exportStockExcel(request):

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    format = workbook.add_format({'num_format': 'dd/mm/yy'})
    worksheet.write('A1', 'Customer Name')
    worksheet.write('B1', 'Sales Order')
    worksheet.write('C1', 'Order Date')
    worksheet.write('D1', 'Item Code')
    worksheet.write('E1', 'Order Qty')
    worksheet.write('F1', 'Supplier Name')
    worksheet.write('G1', 'Required Qty')
    worksheet.write('H1', 'Recieved Qty')
    worksheet.write('I1', 'PO Number')
    worksheet.write('J1', 'Stock Inward Estimate Date')
    worksheet.write('K1', 'Latest Stock Inward Actual Date')
    col = ['A','B','C','D','E','F','G','H','I','J','K']
    rowNo = 1
    allData = StockRequirement.objects.all().values_list('order__customer_name','order__sales_order','order__order_date','order__item_code','order__order_qty','supplier_name','required_qty','recieved_qty','po_number','stock_inward_estimate_date','latest_stock_inward_actual_date')
    for data in allData:
        rowNo+=1
        for row in range(len(data)):
            worksheet.write(str(col[row]+str(rowNo)),str(data[row]),format)
    workbook.close()

    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="stock_requirement.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response

@login_required(login_url='login')
def stockRequirement(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    stockDetails = StockRequirement.objects.all()
    suppliers = Supplier.objects.all()
    context = {
        'consoleName':consoleName,
        'stockDetails':stockDetails,
        'suppliers':suppliers
    }
    return render(request,'pms/stock_requirement.html',context)

@login_required(login_url='login')
def addSupplier(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        gst = request.POST['gst']
        pan = request.POST['pan']
        address = request.POST['address']
        newSupplier = Supplier(name=name,email=email,phone=contact,gst_no=gst,pan_no=pan,address=address)
        newSupplier.save()
    context = {
        'consoleName':consoleName
    }
    return render(request,'pms/add_supplier.html',context)



@login_required(login_url='login')
def updateStockRequirement(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    if request.method=='POST':
        id = request.POST['id']
        estimate_date = request.POST['estimate_date']
        actual_date = request.POST['actual_date']
        supplier_name = request.POST['supplier_name']
        received_qty = request.POST['qty_recieved']
        po_num = request.POST['po_num']
        stock = StockRequirement.objects.filter(id=id).first()
        if estimate_date:
            stock.stock_inward_estimate_date = estimate_date
            
        if actual_date:
            stock.latest_stock_inward_actual_date = actual_date
            
        if supplier_name:
            stock.supplier_name=supplier_name
            
        if int(received_qty)>0:
            inventory = Inventory.objects.filter(item_code=stock.order.item_code).first()
            inventory.opening_qty = inventory.balanced_qty
            inventory.added_qty = received_qty
            inventory.balanced_qty += int(received_qty)
            inventory.save() 
            stock.required_qty = int(stock.required_qty) - int(received_qty)
            stock.recieved_qty = received_qty
            
        if po_num:
            stock.po_number = po_num
        stock.save()
        
    return redirect('stockRequirement',consoleName)
