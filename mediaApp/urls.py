from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = "home"),
    path('base/', views.base_view, name = 'base'),
    path('register/', views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='mediaApp/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile_post/', views.profile_list, name = "profile_post"),
    path('create_post/', views.create_post, name = "create_post"),
    path('edit_post/<int:pk>/', views.edit_post, name = "edit_post"),
    path('delete_post/<int:pk>/', views.delete_post, name = "delete_post"),
    path('category/<str:category_name>/', views.category_posts, name = "category_posts"),
    
]