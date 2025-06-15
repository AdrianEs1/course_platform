from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('courselist/', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('edit/<int:course_id>', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('addmodule/<int:course_id>', views.add_module, name='add_module'),
    path('coursedetail/<int:course_id>', views.course_detail, name='course_detail'),
    path('editmodule/<int:module_id>', views.edit_module, name='edit_module'),
    path('deletemodule/<int:module_id>', views.delete_module, name='delete_module'),
    path('agregarcourse/<int:course_id>', views.agregarcourse, name='agregarcourse'),
    path('coursestudent/', views.coursestudent, name='coursestudent'),
    path('courseteacher/', views.courseteacher, name='courseteacher'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]