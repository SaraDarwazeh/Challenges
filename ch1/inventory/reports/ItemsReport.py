from inventory.models import Order_Item
class ItemsReport:
    def build_items_report(self):
        qs = Order_Item.objects.all()
        return qs