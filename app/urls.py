from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homepage, name = 'homepage'),
    path('adminhome',views.adminhome, name = 'adminhome'),
    path('admin_login',views.admin_login, name = 'admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('change_password', views.change_password, name='change_password'),
    path('managecontent/',views.managecontent, name = 'managecontent'),
    path('update_content/', views.update_content, name='update_content'),
    path('manageskills/', views.manageskills, name='manageskills'),
    path('admin/skills/add/', views.add_skill, name='add_skill'),
    path('admin/skills/update/', views.update_skill, name='update_skill'),
    path('admin/skills/delete/', views.delete_skill, name='delete_skill'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)