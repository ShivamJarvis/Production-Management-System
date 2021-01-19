from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from mainApp.models import UserData
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
    context = {
        'consoleName':consoleName
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

