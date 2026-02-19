from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-payment/', views.start_payment, name='start_payment'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
]
