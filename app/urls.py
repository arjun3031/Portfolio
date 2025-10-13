from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name = 'homepage'),
    path('adminhome',views.adminhome, name = 'adminhome')
]
