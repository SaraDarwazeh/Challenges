import time
from django.http import JsonResponse
from inventory.reports import SalesDetailsReport
from django.views import View

class SalesDetailsView(View):
    def get(self, request):
        qs = SalesDetailsReport().build_queryset()
        rows = qs.values()

        start = time.perf_counter()
        data = list(rows)  
        end = time.perf_counter()
        print(f"Query execution time: {end - start} seconds")

        return JsonResponse({"data": data})