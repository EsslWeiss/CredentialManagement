from django.urls import path
from .views import customers_list, customer_detail

urlpatterns = [
    path('customers/', customers_list),
    path('customer/<int:pk>/', customer_detail),
]
