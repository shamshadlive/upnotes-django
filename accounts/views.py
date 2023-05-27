from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms  import UserForm
from django.contrib.auth import authenticate,login,logout

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