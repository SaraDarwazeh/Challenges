from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
import random

from inventory.models import Item, Order, Order_Item


MILLION = 1_000_000


class Command(BaseCommand):
    help = "Seed database with lots of items, orders, and order items"

    def add_arguments(self, parser):
        # Old (still supported)
        parser.add_argument("--items", type=int, default=200)
        parser.add_argument("--orders", type=int, default=1000)

        # New: multiples of a million
        parser.add_argument("--items-m", type=int, default=0, help="Items in millions (e.g. 2 => 2,000,000)")
        parser.add_argument("--orders-m", type=int, default=0, help="Orders in millions (e.g. 1 => 1,000,000)")

        parser.add_argument("--min-lines", type=int, default=1)
        parser.add_argument("--max-lines", type=int, default=10)

        parser.add_argument("--batch-size", type=int, default=10_000)
        parser.add_argument("--wipe", action="store_true")

    def handle(self, *args, **opts):
        # Decide counts
        items_count = opts["items_m"] * MILLION if opts["items_m"] else opts["items"]
        orders_count = opts["orders_m"] * MILLION if opts["orders_m"] else opts["orders"]

        min_lines = opts["min_lines"]
        max_lines = opts["max_lines"]
        batch_size = opts["batch_size"]
        wipe = opts["wipe"]

        if wipe:
            Order_Item.objects.all().delete()
            Order.objects.all().delete()
            Item.objects.all().delete()
            self.stdout.write(self.style.WARNING("Wiped old data."))

        self.stdout.write(self.style.NOTICE(f"Seeding: items={items_count:,}, orders={orders_count:,}"))

        # -------- Items (batched) --------
        with transaction.atomic():
            buf = []
            for i in range(1, items_count + 1):
                buf.append(
                    Item(
                        name=f"Item {i}",
                        sell_price=Decimal(random.randint(5, 2000)),
                        stock=random.randint(0, 2000),
                    )
                )
                if len(buf) >= batch_size:
                    Item.objects.bulk_create(buf, batch_size=batch_size)
                    buf.clear()
            if buf:
                Item.objects.bulk_create(buf, batch_size=batch_size)

        item_ids = list(Item.objects.values_list("id", flat=True))
        self.stdout.write(self.style.SUCCESS(f"Items: {len(item_ids):,}"))

        # -------- Orders (batched) --------
        with transaction.atomic():
            buf = []
            for _ in range(orders_count):
                buf.append(Order())
                if len(buf) >= batch_size:
                    Order.objects.bulk_create(buf, batch_size=batch_size)
                    buf.clear()
            if buf:
                Order.objects.bulk_create(buf, batch_size=batch_size)

        order_ids = list(Order.objects.values_list("id", flat=True))
        self.stdout.write(self.style.SUCCESS(f"Orders: {len(order_ids):,}"))

        # -------- Order items (batched) --------
        # IMPORTANT: هذا الجزء هو اللي ممكن يعمل رقم مهول جدًا
        # مثال: 1,000,000 orders * متوسط 5 lines = 5,000,000 order_items
        with transaction.atomic():
            buf = []
            for oid in order_ids:
                lines = random.randint(min_lines, max_lines)
                for _ in range(lines):
                    iid = random.choice(item_ids)
                    quantity = random.randint(1, 20)

                    # لو بدك سعر الوحدة random فوق سعر البيع
                    # (ملاحظة: إذا item.sell_price مش متاح هون لأنه ما جبنا objects)
                    # نعمل سعر وهمي ثابت/عشوائي:
                    unit_price = Decimal(random.randint(5, 2500))

                    buf.append(
                        Order_Item(
                            order_id=oid,
                            item_id=iid,
                            unit_price=unit_price,
                            quantity=quantity,
                        )
                    )

                    if len(buf) >= batch_size:
                        Order_Item.objects.bulk_create(buf, batch_size=batch_size)
                        buf.clear()

            if buf:
                Order_Item.objects.bulk_create(buf, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"Order Items: {Order_Item.objects.count():,}"))
