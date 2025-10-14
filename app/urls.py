from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name = 'homepage'),
    path('adminhome',views.adminhome, name = 'adminhome'),
    path('admin_login',views.admin_login, name = 'admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('change_password', views.change_password, name='change_password'),
]
