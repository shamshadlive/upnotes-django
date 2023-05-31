from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms  import UserForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q

from django.views.decorators.cache import cache_control
# Create your views here.

def login_page (request):
    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login')
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/notes')
            # return render(request, 'notes/notes.html')
            
    
    return render(request, 'accounts/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    form = UserForm()
    context = {'form':form}
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            ) 
            user.save()
            messages.success(request, "Account Created Succesfuly")
            return redirect('/login')
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserForm()
           
    return render(request, 'accounts/register.html',context)


def logout_page(request):
    logout(request)
    return redirect('/')


#admin section


def admincontrolLogin(request):
    
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        if not User.objects.filter(Q(username=username) & Q(is_superuser=1)).exists():
            messages.error(request, "Invalid Username of admin")
            return redirect('admin_login')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('admin_login')
        else:
            login(request,user)
            next_url = request.GET.get('next')  # Get the "next" parameter from the form
            print("=================")
            print(next_url)
            if next_url:
                print("++++++++++")   
                return redirect(next_url)
            
            return redirect('admin_control')
        
    if request.user.is_authenticated and  request.user.is_superuser:
        return redirect('admin_control')
    if request.user.is_authenticated:
        messages.error(request, "You logined using another account ! Login as admin to access admin page")
        return render(request,'accounts/admin_login.html')
    
    
    return render(request,'accounts/admin_login.html')

def admincontrolRegister(request):
    if request.user.is_authenticated and  (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_control')
    
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            user.is_staff = 1 
            user.is_superuser = 1
            user.save()
            messages.success(request, "Account Created Succesfuly")
            return redirect('admin_login')
        else:
            return render(request, 'accounts/admin_register.html', {'form': form})
    else:
        form = UserForm()
    context = {'form':form}
    
    return render(request,'accounts/admin_register.html',context)


