"""PROSOR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from .views import project, user, add_project,team_project_detail,complete_project_detail,home_page, not_found


urlpatterns = [
     path('', home_page.as_view(), name='home_page'), # home page for admin user
     path('project/<str:page>', project.as_view(), name='projects'), #project/assigned , project/queued
     path('ourwork/<str:id>', complete_project_detail.as_view(), name='ourwork'), 
     path('addproject/', add_project.as_view(), name='add_project'),
     path('projectdetail/<str:id>', team_project_detail.as_view(), name='team_project_detail'),   
     path('editproject/<str:id>', views.edit_project, name='edit_project'), 
     path('user/', user.as_view(), name='user'),
     path('adduser/', views.add_user, name='add_user'),
     path('contactus/', views.contact_us, name='contact_us'),
     path('edituser/<str:email>/', views.edit_user, name='edit_user'), 
     path('userprofile/<str:email>/', views.user_profile, name='user_profile'),
     path('ajax/ApplicationDataUpdate/', views.ApplicationDataUpdate, name='ApplicationDataUpdate'), 
     path('404', views.not_found, name='not_found'),
     path('product/<id>', views.product, name='product'),
]
