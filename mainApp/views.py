from io import BytesIO
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from mainApp.models import Inventory, Job, Order, ProvisionalSchedule, Supplier, UserData, StockRequirement
import pandas as pd
import xlsxwriter
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from datetime import date, datetime
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

    salesOrder =[]
    customerName = []
    itemCode = []
    for data in orderData:
            if not  data.qty_in_engineering == data.order_qty and not data.qty_in_buffing == data.order_qty and not data.qty_in_provisionally_schedule == data.order_qty and not data.qty_in_plating == data.order_qty and not data.qty_in_4sbuffing == data.order_qty and not data.qty_in_laquer == data.order_qty and not data.qty_in_packaging == data.order_qty:
                if not  data.customer_name in customerName:
                    customerName.append(data.customer_name)
                if not data.sales_order in salesOrder:
                    salesOrder.append(data.sales_order)
                if not data.item_code in itemCode:
                    itemCode.append(data.item_code)
            deliveryDate = data.item_delivery_date
            remainingDaysForDelivery = deliveryDate - date.today()
            data.remaining_days_delivery = remainingDaysForDelivery.days
            completeDate =  data.completed_date
            if completeDate:
                remaingForCompletion =  date.today() - completeDate
                if remaingForCompletion.days == 2:
                    data.completed = True
            data.save()


    context = {
        'consoleName':consoleName,
        'orderData':orderData,
     
        'customerName':customerName,
        'salesOrder':salesOrder,
        'itemCode':itemCode
    }
    return render(request,'pms/order_summary.html',context)


@login_required(login_url='login')
def provisionalSchedule(request,consoleName):
    user = request.user
    userData = UserData.objects.filter(user=user).all()
    for user in userData:
        if not user.permission == consoleName:
            return redirect('consoles')
    provisionalSchedules = ProvisionalSchedule.objects.all()
    for data in provisionalSchedules:
        stockRequirement = StockRequirement.objects.filter(order=data.order).first()
        if stockRequirement:
            if stockRequirement.pending_qty < data.qty:
                data.is_material_required = False
                data.save()
    context = {
        'consoleName':consoleName,
        'provisionalSchedule':provisionalSchedules
    }
    return render(request,'pms/provisional_schedule.html',context)



@login_required(login_url='login')
def orderHistory(request,consoleName):
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
            data = pd.read_excel('media/'+filename,engine='openpyxl')
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
                remainingDaysForDelivery = deliveryDate.date() - date.today()
                newOrder = Order(order_type=orderType,sales_order=salesOrderNo,customer_name=customerName,order_date=orderDate,item_code=itemCode,item_delivery_date=deliveryDate,order_qty=orderQuantity,description=description,status='Pending',remaining_days_delivery=remainingDaysForDelivery.days)
                newOrder.save()
                inventory = Inventory.objects.filter(item_code = itemCode).first()
                # For Direct Orders
                if inventory and orderType == 'Direct':
                    newOrder.inventory = inventory
                    newOrder.save()
                    if orderQuantity>inventory.reserve_qty:
                        requiredQtyForDirectOrders = orderQuantity - inventory.reserve_qty
                    else:
                        requiredQtyForDirectOrders = 0
                    
                    if requiredQtyForDirectOrders>0:
                        newStockRequirement = StockRequirement(order=newOrder,item_code=itemCode,required_qty = requiredQtyForDirectOrders, recieved_qty=0, pending_qty=requiredQtyForDirectOrders)
                        newStockRequirement.save()

                        newOrder.for_dispatch = orderQuantity - requiredQtyForDirectOrders
                        newOrder.save()
                    else:
                        newOrder.for_dispatch = orderQuantity 
                        newOrder.save()
                    inventory.reserve_qty -= orderQuantity
                    inventory.save()
                    if inventory.reserve_qty<0:
                        inventory.reserve_qty = 0
                        inventory.save()
                elif not inventory and orderType == 'Direct':
                    newInventory = Inventory(item_code=itemCode,opening_qty=0,added_qty=0,issued_dispatched_qty=0,reserve_qty=0,balanced_qty=0)
                    newInventory.save()
                    newOrder.inventory = newInventory
                    newOrder.save()
                    newStockRequirement = StockRequirement(order=newOrder,item_code=itemCode,required_qty = orderQuantity, recieved_qty=0, pending_qty=orderQuantity)
                    newStockRequirement.save()
                
                # For Others Orders
                elif inventory and orderType == 'Others':
                    newOrder.inventory = inventory
                    newOrder.save()
                    if orderQuantity>inventory.reserve_qty:
                        stockRequirementForOthers = orderQuantity - inventory.reserve_qty
                    else:
                        stockRequirementForOthers = 0
                        newOrder.for_dispatch = orderQuantity 
                        newOrder.save()
                    if stockRequirementForOthers>0:
                        newOrder.for_dispatch = orderQuantity - stockRequirementForOthers
                        newOrder.save()
                    else:
                        newOrder.for_dispatch = orderQuantity
                        newOrder.save()


                    if stockRequirementForOthers > 0:
                        rawInventory = Inventory.objects.filter(item_code=inventory.item_code[:-2]+'RW').first()
                        if rawInventory:
                            if stockRequirementForOthers>rawInventory.reserve_qty:
                                rawQuantityIsRequired = stockRequirementForOthers - rawInventory.reserve_qty
                            else:
                                rawQuantityIsRequired = 0
                            
                            if rawQuantityIsRequired>0:
                                newStockRequirement = StockRequirement(order=newOrder,item_code=rawInventory.item_code,required_qty=rawQuantityIsRequired,pending_qty=rawQuantityIsRequired,recieved_qty=0)
                                newStockRequirement.save()
                            rawInventory.reserve_qty -= rawQuantityIsRequired
                            if rawInventory.reserve_qty < 0:
                                rawInventory.reserve_qty = 0
                            rawInventory.save() 
                        else:
                            newRawInventory = Inventory(item_code=inventory.item_code[:-2]+'RW',opening_qty=0,added_qty=0,issued_dispatched_qty=0,reserve_qty=0,balanced_qty=0)
                            newRawInventory.save()
                            newStockRequirement = StockRequirement(order=newOrder,item_code=newRawInventory.item_code,required_qty=stockRequirementForOthers,pending_qty=stockRequirementForOthers,recieved_qty=0)
                            newStockRequirement.save()
                        

                    
                    inventory.reserve_qty -= orderQuantity
                    inventory.save()
                    if inventory.reserve_qty<0:
                        inventory.reserve_qty = 0
                        inventory.save()
                
                elif not inventory and orderType == 'Others':
                    newFinishInventory = Inventory(item_code=itemCode,opening_qty=0,added_qty=0,issued_dispatched_qty=0,reserve_qty=0,balanced_qty=0)
                    newFinishInventory.save()
                    newOrder.inventory = newFinishInventory
                    newOrder.save()
                    rawInventory = Inventory.objects.filter(item_code=itemCode[:-2]+'RW').first()
                    if rawInventory:
                        if orderQuantity>rawInventory.reserve_qty:
                            rawQuantityIsRequired = orderQuantity - rawInventory.reserve_qty
                        else:
                            rawQuantityIsRequired = 0
                        
                        if rawQuantityIsRequired>0:
                            newStockRequirement = StockRequirement(order=newOrder,item_code=rawInventory.item_code,required_qty=rawQuantityIsRequired,pending_qty=rawQuantityIsRequired,recieved_qty=0)
                            newStockRequirement.save()
                        rawInventory.reserve_qty -= rawQuantityIsRequired
                        if rawInventory.reserve_qty < 0:
                            rawInventory.reserve_qty = 0
                        rawInventory.save() 
                    else:
                        newRawInventory = Inventory(item_code=itemCode[:-2]+'RW',opening_qty=0,added_qty=0,issued_dispatched_qty=0,reserve_qty=0,balanced_qty=0)
                        newRawInventory.save()
                        newStockRequirement = StockRequirement(order=newOrder,item_code=newRawInventory.item_code,required_qty=orderQuantity,pending_qty=orderQuantity,recieved_qty=0)
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
            data = pd.read_excel('media/'+filename,engine='openpyxl')
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
                    item = Inventory(item_code=itemCode,opening_qty=openingQty,added_qty=addedQty,issued_dispatched_qty=issuedQty,balanced_qty=balanceQty,reserve_qty=balanceQty)
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
            stock.recieved_qty += int(received_qty)
            stock.order.for_dispatch += int(received_qty)
            stock.order.save()
            stock.pending_qty -= int(received_qty) 
        if po_num:
            stock.po_number = po_num
        stock.save()
        
    return redirect('stockRequirement',consoleName)

@login_required(login_url='login')
def orderDispatch(request,consoleName,orderId):
    order = Order.objects.filter(id=orderId).first()
    inventory = Inventory.objects.filter(item_code=order.item_code).first()
    rawInventory = Inventory.objects.filter(item_code=order.item_code[:-2]+"RW").first()
    stockRequirement = StockRequirement.objects.filter(order=order).first()
    maxToDispatch = order.order_qty
    if stockRequirement:
        maxToDispatch -= stockRequirement.required_qty
        if rawInventory:
            maxToDispatch -= rawInventory.balanced_qty
    
    if request.method == 'POST':
        dispatchValue = request.POST['dispatch']
        if dispatchValue == 'dispatchA':
            qty = order.order_qty - order.total_processed_qty
            order.total_processed_qty += qty
            order.qty_in_packaging += qty
            order.status = 'Completed'
            order.completed_date = date.today()
            order.save()
            inventory = Inventory.objects.filter(item_code=order.item_code).first()
            inventory.opening_qty = inventory.balanced_qty
            inventory.issued_dispatched_qty = qty
            inventory.balanced_qty -= inventory.issued_dispatched_qty
            inventory.save()
            id = 0
            allJob = Job.objects.all()
            if not allJob:
                id = 1
            else:
                id = len(allJob)+1
            id = "000/"+str(id)+"/"+order.order_type
            newJob = Job(job_id = id, order=order,department="Packaging",qty=qty,date=date.today())
            newJob.save()
        elif dispatchValue == 'dispatchP':
            qty = int(request.POST['qty'])
            order.qty_in_packaging += qty
            order.latest_partially_dispatched_qty = qty
            order.latest_partially_dispatched_date = date.today()
            order.partially_dispatched_qty += qty
            order.for_dispatch -= qty 
            order.total_processed_qty += qty
            order.status = 'Partially Dispatched'
            if order.qty_in_packaging == order.order_qty:
                order.status = 'Completed'
                order.completed_date = date.today()
            order.save()
            inventory = Inventory.objects.filter(item_code=order.item_code).first()
            inventory.opening_qty = inventory.balanced_qty
            inventory.issued_dispatched_qty = qty
            inventory.balanced_qty -= inventory.issued_dispatched_qty
            inventory.save()
            allJob = Job.objects.all()
            if not allJob:
                id = 0
            else:
                id = len(allJob)+1
            id = "000/"+str(id)+"/"+order.order_type
            newJob = Job(job_id = id, order=order,department="Packaging",qty=qty,date=date.today())
            newJob.save()
        return redirect('orderSummary',consoleName)
    stockRequirement = StockRequirement.objects.filter(order=order).first()
    context = {
        'item':inventory,
        'order':order,
        'maxToDispatch':maxToDispatch,
        'orderId':orderId,
        'consoleName':consoleName,
        'stockRequirement':stockRequirement
    }
    return render(request,'pms/order_dispatch.html',context)

@login_required(login_url='login')
def orderUpdatePaymentStatus(request,consoleName):
    if request.method=='POST':
        id = request.POST['id']
        order = Order.objects.filter(id=id).first()
        status = request.POST['payment_status']
        order.payment_staus = status
        order.save()
    return redirect('orderSummary',consoleName)

@login_required(login_url='login')
def orderCancel(request,consoleName):
    if request.method == 'POST':
        allId = request.POST['ids']
        allId = allId.split(',')
        for id in allId:
            order = Order.objects.filter(id=int(id)).first()
            order.status = "Canceled"
            try:
                stock = StockRequirement.objects.filter(order=order).first()
                stock.delete()
            except:
                pass
            order.save()
    return redirect('orderSummary',consoleName)

@login_required(login_url='login')
def uploadStockRequirement(request,consoleName):
    if request.method == 'POST':
        stockRequirement = StockRequirement.objects.all()
        stockFile = request.FILES['stock_file']
        fs = FileSystemStorage()
        filename = fs.save(stockFile.name,stockFile) 

        stockData = pd.read_excel('media/'+filename,engine='openpyxl')     
        stockData['Purchase Order'] = stockData['Purchase Order'].fillna('NA')
        for stock in range (0,len(stockData)):
            if not stockData['Purchase Order'][stock] == 'NA':
  
                for data in stockRequirement:
                    if data.po_number:
                        print(stockData['Purchase Order'][stock])
                        if data.po_number == stockData['Purchase Order'][stock] and data.order.item_code == stockData['Item Code'][stock]:
                            data.recieved_qty += int(stockData['Stock Qty'][stock])
                            inventory = Inventory.objects.filter(item_code=data.order.item_code).first()
                            inventory.opening_qty = inventory.balanced_qty 
                            inventory.added_qty = data.recieved_qty

                            inventory.balanced_qty += inventory.added_qty 
                            inventory.reserve_qty = inventory.balanced_qty
                            inventory.save()
                     
                            if data.recieved_qty < data.required_qty:
                                data.pending_qty = data.required_qty - data.recieved_qty

                        data.save()
                
    return redirect('stockRequirement',consoleName)

@login_required(login_url='login')
def listSupplier(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        supplier = Supplier.objects.filter(id=id).first()
        supplier.name = request.POST['name']
        supplier.email = request.POST['email']
        supplier.phone = request.POST['phone']
        supplier.gst_no = request.POST['gst']
        supplier.pan_no = request.POST['pan']
        supplier.address = request.POST['address']
        supplier.save()

    supplierData = Supplier.objects.all()
    context = {
        'consoleName' : consoleName,
        'supplierData':supplierData
    }
    return render(request,'pms/edit_supplier.html',context)

@login_required(login_url='login')
def orderSchedule(request,consoleName,orderId):
    if request.method == 'POST':
        order = Order.objects.filter(id=orderId).first()
        qty = int(request.POST['qty'])
        from_inventory = False
        if qty>0:
            order.total_processed_qty += int(qty)
            order.qty_in_provisionally_schedule += int(qty)
            inventory = Inventory.objects.filter(item_code=order.item_code[:-2]+'RW').first()
            
            if inventory.balanced_qty < int(qty):
                inventory.balanced_qty = 0
            else:
                from_inventory = True
                inventory.opening_qty = inventory.balanced_qty
                inventory.issued_dispatched_qty = int(qty)
                inventory.balanced_qty -= int(qty)
            inventory.save()
            order.save()
            pDate = request.POST['date']
            allJob = Job.objects.all()
            if not allJob:
                id = 1
            else:
                id = len(allJob)+1
            id = "000/"+str(id)+"/"+order.order_type
            newJob = Job(job_id=id,order=order,department='Production',qty=qty,date=date.today())
            newJob.save()
            stock = StockRequirement.objects.filter(order=order).first()
            stock_required=False
            if stock:
                if stock.stock_inward_estimate_date:
                    stock_required=True
            newProvisionalSchedule = ProvisionalSchedule(job=newJob,order=order,provision_date=pDate,qty=qty,stock=stock,is_material_required=stock_required,from_inventory=from_inventory)
            newProvisionalSchedule.save()

    order = Order.objects.filter(id=orderId).first()
    inventory = Inventory.objects.filter(item_code=order.item_code).first()
    rawStock = StockRequirement.objects.filter(order=order).first()
    rawInventory = Inventory.objects.filter(item_code=order.item_code[:-2]+'RW').first()
    maxToDispatch = order.order_qty
    if rawStock:
        maxToDispatch -= rawStock.required_qty
        if rawInventory:
            maxToDispatch -= rawInventory.balanced_qty

   

    context = {
        'consoleName':consoleName,
        'order':order,
        'rawInventory':rawInventory,
        'rawStock':rawStock,
        'inventory':inventory,
        'maxToDispatch':maxToDispatch
    }
    return render(request,'pms/schedule_provisionally.html',context)

@login_required(login_url='login')
def deleteProvisionalSchedule(request,consoleName):
    if request.method == 'POST':
        try:
            provsionalId = request.POST['selectedJobs'].split(',')
            for id in provsionalId:
                provisionalSchedule = ProvisionalSchedule.objects.filter(id=id).first()
                if not provisionalSchedule.from_inventory: # Based on Estimate Date
                    provisionalSchedule.order.total_processed_qty -= provisionalSchedule.qty
                    provisionalSchedule.order.qty_in_provisionally_schedule -= provisionalSchedule.qty
                    provisionalSchedule.order.status = 'Pending'
                    provisionalSchedule.order.save()
                    provisionalSchedule.job.delete()
                    provisionalSchedule.delete()
                else: # Not Based on Estimate Date, Actually Raw Inventory is available
                    provisionalSchedule.order.total_processed_qty -= provisionalSchedule.qty
                    provisionalSchedule.order.qty_in_provisionally_schedule -= provisionalSchedule.qty
                    inventory = Inventory.objects.filter(item_code=provisionalSchedule.order.item_code[:-2]+"RW").first()
                    inventory.opening_qty = inventory.balanced_qty
                    inventory.added_qty = provisionalSchedule.qty
                    inventory.issued_dispatched_qty -= provisionalSchedule.qty
                    inventory.balanced_qty = (inventory.opening_qty + inventory.added_qty)
                    inventory.save() 
                    provisionalSchedule.order.status = 'Pending'
                    provisionalSchedule.order.save()
                    # provisionalSchedule.job.delete()
                    provisionalSchedule.is_canceled = True
                    provisionalSchedule.save()
        except:
            pass
    return redirect('provisionalSchedule',consoleName)

@login_required(login_url='login')
def finalProvisionalSchedule(request,consoleName):
    if request.method == 'POST':
      
        provisionalId = request.POST['selectedJobs'].split(',')
        for id in provisionalId:
            provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
            if provisionalSchedule.order.order_type == 'Engineering' and not provisionalSchedule.is_material_required:
                provisionalSchedule.order.qty_in_engineering += provisionalSchedule.qty
                provisionalSchedule.order.qty_in_provisionally_schedule -= provisionalSchedule.qty
                provisionalSchedule.job.department = 'Engineering'
                provisionalSchedule.is_finalised = True
                provisionalSchedule.final_date = date.today()
                provisionalSchedule.save()
                provisionalSchedule.order.save()
                provisionalSchedule.job.save()

            elif provisionalSchedule.order.order_type == 'Others' and not provisionalSchedule.is_material_required:
                provisionalSchedule.order.qty_in_buffing += provisionalSchedule.qty
                provisionalSchedule.order.qty_in_provisionally_schedule -= provisionalSchedule.qty
                provisionalSchedule.job.department = 'Buffing'
                provisionalSchedule.is_finalised = True
                provisionalSchedule.final_date = date.today()
                provisionalSchedule.save()
                provisionalSchedule.order.save()
                provisionalSchedule.job.save()
      
          
    return redirect('provisionalSchedule',consoleName)

@login_required(login_url='login')
def orderUpdateType(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        orderType = request.POST['order_type']
        order = Order.objects.filter(id=id).first()
        order.order_type = orderType
        order.save()
    return redirect('orderSummary',consoleName)

@login_required(login_url='login')
def buffingOrders(request,consoleName):
    provisionalData = ProvisionalSchedule.objects.filter(final_date=date.today()).all()
    context = {
        'consoleName':consoleName,
        'provisionalData':provisionalData
    }
    return render(request,'pms/buffing_orders.html',context)


@login_required(login_url='login')
def completeBuffingOrders(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.job.department = 'Plating'
        provisionalSchedule.order.qty_in_buffing -= provisionalSchedule.job.qty
        provisionalSchedule.order.qty_in_plating += provisionalSchedule.job.qty
        provisionalSchedule.order.save()
        provisionalSchedule.job.save()

    return redirect('buffingOrders',consoleName)

@login_required(login_url='login')
def platingOrders(request,consoleName):
    provisionalData = ProvisionalSchedule.objects.all()
    context = {
        'consoleName':consoleName,
        'provisionalData':provisionalData
    }
    return render(request,'pms/plating_orders.html',context)

@login_required(login_url='login')
def completePlatingOrders(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.job.department = '4S Buffing'
        provisionalSchedule.order.qty_in_plating -= provisionalSchedule.job.qty
        provisionalSchedule.order.qty_in_4sbuffing += provisionalSchedule.job.qty
        provisionalSchedule.order.save()
        provisionalSchedule.job.save()

    return redirect('buffingOrders',consoleName)

@login_required(login_url='login')
def sBuffingOrders(request,consoleName):
    provisionalData = ProvisionalSchedule.objects.all()
    context = {
        'consoleName':consoleName,
        'provisionalData':provisionalData
    }
    return render(request,'pms/sBuffing.html',context)

@login_required(login_url='login')
def complete4SBuffingOrders(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.job.department = 'Laquer'
        provisionalSchedule.order.qty_in_4sbuffing -= provisionalSchedule.job.qty
        provisionalSchedule.order.qty_in_laquer += provisionalSchedule.job.qty
        provisionalSchedule.order.save()
        provisionalSchedule.job.save()

    return redirect('sBuffingOrders',consoleName)

@login_required(login_url='login')
def laquerOrders(request,consoleName):
    provisionalData = ProvisionalSchedule.objects.all()
    context = {
        'consoleName':consoleName,
        'provisionalData':provisionalData
    }
    return render(request,'pms/laquer_order.html',context)

@login_required(login_url='login')
def completeLaquerOrders(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.job.department = 'Packaging'
        provisionalSchedule.order.qty_in_laquer -= provisionalSchedule.job.qty
        provisionalSchedule.order.qty_in_packaging += provisionalSchedule.job.qty
        provisionalSchedule.order.save()
        provisionalSchedule.job.save()
    return redirect('laquerOrders',consoleName)

@login_required(login_url='login')
def engineeringOrders(request,consoleName):
    provisionalData = ProvisionalSchedule.objects.all()
    context = {
        'consoleName':consoleName,
        'provisionalData':provisionalData
    }
    return render(request,'pms/engineering_order.html',context)

@login_required(login_url='login')
def completeEngineeringOrders(request,consoleName):
    if request.method == 'POST':
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.job.department = 'Packaging'
        provisionalSchedule.order.qty_in_engineering -= provisionalSchedule.job.qty
        provisionalSchedule.order.qty_in_packaging += provisionalSchedule.job.qty
        provisionalSchedule.order.save()
        provisionalSchedule.job.save()
    return redirect('engineeringOrders',consoleName)

@login_required(login_url='login')
def packagingOrders(request,consoleName):
    jobData = Job.objects.filter(department='Packaging').all()
    context = {
        'consoleName':consoleName,
        'jobData':jobData
    }
    return render(request,'pms/packaging_order.html',context)

@login_required(login_url='login')
def completePackagingOrders(request,consoleName):

    if request.method == 'POST':
        id = request.POST['id']
        job = Job.objects.filter(id=int(id)).first()
        job.department = "Completed"
        job.save()
        if job.order.order_qty == job.order.qty_in_packaging:
            job.order.status = "Completed"
            job.order.completed_date = date.today()
            job.order.save()
    return redirect('packagingOrders',consoleName)

def updateProvisionalSchedule(request,consoleName):
    if request.method == 'POST':
        qty = int(request.POST['qty'])
        date = request.POST['date']
        id = request.POST['id']
        provisionalSchedule = ProvisionalSchedule.objects.filter(id=int(id)).first()
        provisionalSchedule.provision_date = date
        if not provisionalSchedule.qty == qty:
            provisionalSchedule.qty = qty
            provisionalSchedule.job.qty = qty
            provisionalSchedule.order.total_processed_qty -= qty
            provisionalSchedule.order.qty_in_provisionally_schedule -= qty
            provisionalSchedule.order.save()
            provisionalSchedule.job.save()
            if provisionalSchedule.from_inventory:
                inventory = Inventory.objects.filter(item_code=provisionalSchedule.order.item_code[:-2]+'RW').first()
                inventory.opening_qty = inventory.balanced_qty
                inventory.added_qty += qty
                inventory.issued_dispatched_qty -= qty
                inventory.balanced_qty = (inventory.opening_qty + inventory.added_qty)
                inventory.save()
    return redirect('provisionalSchedule',consoleName)