from django.urls import path

from . import views

urlpatterns = [
    path("notes/", views.notes, name="notes"),
    path("notes/create", views.createNote, name="create"),
    path("notes/update/<str:pk>/", views.updateNote, name="update"),
    path("notes/delete/<str:pk>/", views.deleteNote, name="delete"),
    
    #admin
    path("admincontrol/", views.admincontrol, name="admin_control"),
    path("admincontrol/user/create", views.admincontrol_userCreate, name="admin_control_usercreate"),
    path("admincontrol/user/update/<str:pk>/", views.admincontrol_userUpdate, name="admin_control_userupdate"),
    path("admincontrol/user/delete/<str:pk>/", views.admincontrol_userDelete, name="admin_control_userdelete"),
    path("admincontrol/notes/<str:pk>/", views.admincontrol_getUserNote, name="admin_control_usernote"),
    path("admincontrol/notes/<str:pk>/create", views.admincontrol_noteCreate, name="admin_control_note_create"),
    path("admincontrol/notes/<str:pk>/delete", views.admincontrol_noteDelete, name="admincontrol_note_delete"),
    
    
    

    
    
]