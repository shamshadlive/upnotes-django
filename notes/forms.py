from django.forms import ModelForm
from .models import Note
from django.contrib.auth.models import User
class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["title", "body"]
    

class AdminUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","password","email","is_superuser","is_active"]
        
class UpdateAdminUserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username","email","is_superuser","is_active"]
        