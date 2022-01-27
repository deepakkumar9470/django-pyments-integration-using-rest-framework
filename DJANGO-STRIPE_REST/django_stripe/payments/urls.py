
from django.contrib import admin
from django.urls import include, re_path,path
from . import views



# urlpatterns = [
#     re_path(r'^$', views.Home.as_View(), name='home'),
#     path('', views.Home.as_view(), name='home'),
#     path('success/', views.success_page, name='success')
# ]  



urlpatterns = [
    re_path(r'^pay/$', views.Payment, name='payment'),
    re_path(r'^success/$', views.success, name='success'),
    re_path(r'^cancel/$', views.cancel, name='cancel'),
]

