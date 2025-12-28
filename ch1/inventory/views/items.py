from inventory.reports import ItemsReport
from django.http import JsonResponse
from django.views import View
import time 

class ItemsReportView(View):
    def get(self,request):
        qs=ItemsReport().build_items_report()
        rows=qs.values()
        start = time.perf_counter()
        data = list(rows)  
        end = time.perf_counter()
        print(f"Query execution time: {end - start} seconds")
        return JsonResponse({"data": data})