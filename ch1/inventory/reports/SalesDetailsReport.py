from django.db.models import F
from inventory.models import Order_Item


class SalesDetailsReport:
    def build_queryset(self):
        qs = Order_Item.objects.all()
        qs = qs.select_related("item", "order")

        expression = (
            F("unit_price") * F("quantity")- F("quantity") * F("item__sell_price")
        )

        return qs.annotate(profit=expression)