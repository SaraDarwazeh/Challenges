from django.db.models import Sum 
from .SalesDetailsReport import SalesDetailsReport

class orderTransReport:
    def buildـorder_trans(self):
            qs=SalesDetailsReport().build_queryset()
            qs=qs.values("order__id").annotate(
                total_profit=Sum("profit"),
                total_quantity=Sum("quantity")
            ).order_by("order__created_at")
            return qs 

