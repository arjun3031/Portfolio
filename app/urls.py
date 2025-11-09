from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homepage, name = 'homepage'),

    path('adminhome/',views.adminhome, name = 'adminhome'),
    path('admin_login',views.admin_login, name = 'admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('change_password', views.change_password, name='change_password'),

    path('managecontent/',views.managecontent, name = 'managecontent'),
    path('update_content/', views.update_content, name='update_content'),

    path('manageskills/', views.manageskills, name='manageskills'),
    path('manageskills/add/', views.add_skill, name='add_skill'),
    path('manageskills/update/', views.update_skill, name='update_skill'),
    path('manageskills/delete/', views.delete_skill, name='delete_skill'),

    path('manage-experience/', views.manage_experience, name='manage_experience'),
    path('add-experience/', views.add_experience, name='add_experience'),
    path('update-experience/<int:pk>/', views.update_experience, name='update_experience'),
    path('delete-experience/<int:pk>/', views.delete_experience, name='delete_experience'),

    path('locked/', views.account_locked, name='account_locked'),

    path('manage-projects/', views.manage_projects, name='manage_projects'),
    path('add-project/', views.add_project, name='add_project'),
    path('update-project/<int:pk>/', views.update_project, name='update_project'),
    path('delete-project/<int:pk>/', views.delete_project, name='delete_project'),
    
    path('manage-education/', views.manage_education, name='manage_education'),
    path('add-education/', views.add_education, name='add_education'),
    path('update-education/<int:pk>/', views.update_education, name='update_education'),
    path('delete-education/<int:pk>/', views.delete_education, name='delete_education'),

    path('contact/', views.contact_view, name='contact'),
    path('adminhome/enquiry/<int:enquiry_id>/', views.get_enquiry_details, name='get_enquiry_details'),
    path('adminhome/enquiry/<int:enquiry_id>/delete/', views.delete_enquiry, name='delete_enquiry'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)