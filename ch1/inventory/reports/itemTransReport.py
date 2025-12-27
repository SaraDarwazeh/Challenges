from django.db.models import F ,Sum
from .SalesDetailsReport import SalesDetailsReport

class itemTransReport:
    def buildـitem_trans(self):
        qs=SalesDetailsReport().build_queryset()
        qs=qs.values("item__id","item__name").annotate(
            total_profit=Sum("profit"),
            total_quantity=Sum("quantity")
        )
        return qs 