from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Note
from .forms  import NoteForm,AdminUserForm,UpdateAdminUserForm
from django.contrib import messages
from django.db.models import Q
import functools
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
# from django.core import serializers
import json
#decorator for checking admin or not

def check_isadmin(view_func, redirect_url="admin_login"):
    """
        used to check loged one was admin or not
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        messages.error(request, "You need to be loggin as admin to access this page")
        redirect_url_ = reverse(redirect_url)+'?next='+request.path
        return redirect(redirect_url_)
    return wrapper


    
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def notes (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    userNotes = Note.objects.filter(Q(author_id=request.user.id) &
                                    (Q(title__icontains=q) | Q(body__icontains=q))
                                    ).order_by('-updated')
    context = {'userNotes':userNotes}
    return render(request, 'notes/notes.html',{'userNotes':userNotes})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def createNote(request):
    form = NoteForm()
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, "Notes Created 💡")
            return redirect('/notes')
        else:
            return render(request, 'notes/create.html', {'form': form})
        
    context = {'form':form}
    return render(request, 'notes/create.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def updateNote(request,pk):

    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)
    if request.method == 'POST':
        form = NoteForm(request.POST,instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Notes Updated 💡")
            return redirect('/notes')
        else:
            return render(request, 'notes/update.html', {'form': form})
    context = {'form':form}
    return render(request, 'notes/update.html',context)

@login_required(login_url="/login/")
def deleteNote(request,pk):
    note = Note.objects.get(id=pk)
    note.delete()
    messages.error(request, "Notes Deleted ❌")
    return redirect('/notes')

@check_isadmin
def admincontrol(request):
    #ajax to get the user notes
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        userID = request.GET.get('q') if request.GET.get('userid') != None else False
        if userID:
            data_ = Note.objects.filter(Q(author_id=userID)).values('author','title','body','author__first_name').order_by('-updated')
            data = json.dumps(list(data_), indent=4)
        else:
            data_ = Note.objects.values('author','title','body','author__first_name').order_by('-updated')
            # data = serializers.serialize('json', data_)
            data = json.dumps(list(data_), indent=4)
            
    # Get requested data and create data dictionary
        data = {'data':'ok succeeess','real':data}
        # return render(request, 'notes/admin_control.html', data)
        return JsonResponse(data,safe=False)

    users = User.objects.all()
    context = {'users':users}
    
    return render(request,'notes/admin_control.html',context)

@check_isadmin
def admincontrol_getUserNote(request,pk):
    userNotes = Note.objects.filter(Q(author_id=pk)).order_by('-updated')
    user = User.objects.get(id=pk)
    context = {'userNotes':userNotes,'user':user,'pk':pk}
    return render(request, 'notes/admin_view_notes.html',context)


@check_isadmin
def admincontrol_noteCreate(request,pk):
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            user=User.objects.get(id=pk)
            form.instance.author =user
            form.save()
            messages.success(request, "Notes Created 💡")
            return redirect('/admincontrol/notes/'+pk)
        else:
            return render(request, 'notes/admin_notes_create.html', {'form': form})
        
    context = {'form':form}
    return render(request, 'notes/admin_notes_create.html',context)

@check_isadmin
def admincontrol_noteDelete(request,pk):
    note = Note.objects.get(id=pk)
    note.delete()
    messages.error(request, "Notes Deleted ❌")
    return redirect('admin_control')








@check_isadmin
def admincontrol_userCreate(request):
    form = AdminUserForm()
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data["password"]
            )
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_active = form.cleaned_data['is_active'] 
            user.save()
            messages.success(request, "User Created 😃")
            return redirect('admin_control')
        else:
            return render(request, 'notes/admin_user_create.html', {'form': form})
        
    context = {'form':form}
    return render(request, 'notes/admin_user_create.html',context)



@check_isadmin
def admincontrol_userUpdate(request,pk):
    user = User.objects.get(id=pk)
    form = UpdateAdminUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateAdminUserForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_active = form.cleaned_data['is_active'] 
            user.save()
            messages.success(request, "User Updated 💡")
            return redirect('admin_control')
        else:
            messages.error(request, form.errors)
            return render(request, 'notes/admin_user_update.html', {'form': form,'pk':pk})
    context = {'form':form,'pk':pk}
    return render(request, 'notes/admin_user_update.html',context)


@check_isadmin
def admincontrol_userDelete(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    messages.error(request, "User Deleted ❌")
    return redirect('admin_control')