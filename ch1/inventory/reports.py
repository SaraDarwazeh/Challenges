from .models import *
from django.db.models import F ,Sum

def buildـsales_details():
    qs=Order_Item.objects.all()
    qs=qs.select_related('item','Order')
    expression=(F("unit_price")*F("quantity"))-(F("quantity")*F("item__sell_price"))
    qs=qs.annotate(profit=expression)
    return qs 

def buildـitem_trans():
    qs=buildـsales_details()
    qs=qs.values("item__id","item__name").annotate(
        total_profit=Sum("profit"),
        total_quantity=Sum("quantity")
    )
    return qs 

def buildـorder_trans():
    qs=buildـsales_details()
    qs=qs.values("order__id").annotate(
        total_profit=Sum("profit"),
        total_quantity=Sum("quantity")
    ).order_by("order__created_at")
    return qs 

def build_grand_total():
    
    qs = buildـsales_details()
    return qs.aggregate(
        total_profit=Sum('profit'),
    )


