from django.db import models

class Item(models.Model):
    name=models.CharField(max_length=255)
    sell_price=models.DecimalField(max_digits=10 ,decimal_places=2)
    stock=models.IntegerField()

    def __str__(self):
            return self.name

class Order(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order_Item(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name="order")
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name="items")
    unit_price=models.DecimalField(max_digits=10 ,decimal_places=2)
    quantity=models.IntegerField()