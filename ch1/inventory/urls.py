from django.urls import path
from .views import *

urlpatterns = [
    path('transactions/',getـsales_details, name='sales-details'),
    path('transactions/items/',getـitem_transactions, name='item-transactions'),
    path('transactions/orders/',getـorder_transactions, name='order-transactions'),
]