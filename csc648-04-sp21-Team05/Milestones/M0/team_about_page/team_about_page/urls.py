"""team_about_page URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

urlpatterns = [
    path('', views.about, name="about"),
    path('team_members_alec', views.about_team_member_alec, name = 'team_members_alec'),
    #path('team_member_folder', views.about, name="team_member_folder/about_alec.html")
    # path('admin/', admin.site.urls),
    # path('', include('pages.urls'))

    #path('', views.about, name= "about"),
    path('team_members_lakshita', views.about_team_member_lakshita, name = 'team_members_lakshita'),
    path('member_bikram', views.member_bikram, name = 'member_bikram'),
    path('team_members_angelo', views.about_team_member_angelo, name = 'team_members_angelo'),
    path('team_members_benjamin', views.about_team_member_benjamin, name = 'team_members_benjamin'),
    path('team_members_jiaxin', views.about_team_member_jiaxin, name = 'team_members_jiaxin'),
    path('team_members_carmen', views.about_team_member_carmen, name = 'team_members_carmen'),
]
