from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import set_language, project_list, project_detail, close_project, delete_project

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('add_project/', views.add_project, name='add_project'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('set-language/', views.set_language, name='set_language'),
    path('projects/', project_list, name='project_list'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/<int:project_id>/close/', close_project, name='close_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),
]