from django.http import JsonResponse
from django.views import View
import time
from inventory.reports.orderTransReport import orderTransReport

class OrderDetailsView(View):
    def get(self, request):
            qs=orderTransReport().buildـorder_trans()
            rows=qs.values()


            start = time.perf_counter()
            data = list(rows)  
            grand=orderTransReport().buildـorder_trans()
            end = time.perf_counter()
            print(f"Query execution time: {end - start} seconds")

            return JsonResponse({"data":data, "grand_total": grand})
