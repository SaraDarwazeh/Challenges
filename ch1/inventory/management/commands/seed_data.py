from django.core.management.base import BaseCommand
from decimal import Decimal
import random

from inventory.models import Item, Order, Order_Item


class Command(BaseCommand):
    help = "Seed database with lots of items, orders, and order items"

    def add_arguments(self, parser):
        parser.add_argument("--items", type=int, default=200)
        parser.add_argument("--orders", type=int, default=1000)
        parser.add_argument("--min-lines", type=int, default=1)
        parser.add_argument("--max-lines", type=int, default=10)
        parser.add_argument("--wipe", action="store_true")

    def handle(self, *args, **opts):
        items_count = opts["items"]
        orders_count = opts["orders"]
        min_lines = opts["min_lines"]
        max_lines = opts["max_lines"]
        wipe = opts["wipe"]

        if wipe:
            Order_Item.objects.all().delete()
            Order.objects.all().delete()
            Item.objects.all().delete()
            self.stdout.write(self.style.WARNING("Wiped old data."))

        # Items
        items = []
        for i in range(1, items_count + 1):
            items.append(
                Item(
                    name=f"Item {i}",
                    sell_price=Decimal(random.randint(5, 2000)),
                    stock=random.randint(0, 2000),
                )
            )
        Item.objects.bulk_create(items)
        items = list(Item.objects.all())

        # Orders
        orders = [Order() for _ in range(orders_count)]
        Order.objects.bulk_create(orders)
        orders = list(Order.objects.all())

        # Order items
        order_items = []
        for order in orders:
            for _ in range(random.randint(min_lines, max_lines)):
                item = random.choice(items)
                quantity = random.randint(1, 20)
                unit_price = item.sell_price + Decimal(random.randint(1, 500))
                order_items.append(
                    Order_Item(
                        order=order,
                        item=item,
                        unit_price=unit_price,
                        quantity=quantity,
                    )
                )

        Order_Item.objects.bulk_create(order_items)

        self.stdout.write(self.style.SUCCESS(f"Items: {Item.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Orders: {Order.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Order Items: {Order_Item.objects.count()}"))
