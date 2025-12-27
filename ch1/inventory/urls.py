from django.urls import path
from .views import *


urlpatterns = [
    path('transactions/',SalesDetailsView.as_view(), name='sales-details'),
    path('transactions/items/',ItemTransactionsView.as_view(), name='item-transactions'),
    path('transactions/orders/',OrderDetailsView.as_view(), name='order-transactions'),
]