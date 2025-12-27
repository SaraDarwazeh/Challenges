from django.http import JsonResponse
from django.views import View
from inventory.reports.itemTransReport import itemTransReport
import time

class ItemTransactionsView(View):
    def get(self, request):
        qs=itemTransReport().buildـitem_trans()
        rows=qs.values()
        start = time.perf_counter()
        data = list(rows)  
        end = time.perf_counter()
        print(f"Query execution time: {end - start} seconds")

        return JsonResponse({"data":data})


