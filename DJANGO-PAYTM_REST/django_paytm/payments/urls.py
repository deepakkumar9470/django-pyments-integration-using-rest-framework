from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_handle, name='success'),
    
]

