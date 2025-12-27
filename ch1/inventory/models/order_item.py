from django.db import models
from .item import Item
from .order import Order

class Order_Item(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name="order")
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name="items")
    unit_price=models.DecimalField(max_digits=10 ,decimal_places=2)
    quantity=models.IntegerField()