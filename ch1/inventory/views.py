from .models import *
from django.db.models import F 
from django.http import JsonResponse
from .reports import *


def getـsales_details(request):
    qs=buildـsales_details()
    rows=qs.values()
    return JsonResponse({"data":list(rows)})

def getـitem_transactions(request):
    qs=buildـitem_trans()
    rows=qs.values()
    return JsonResponse({"data":list(rows)})

def getـorder_transactions(request):
    qs=buildـorder_trans()
    rows=qs.values()
    grand=build_grand_total()
    return JsonResponse({"data":list(rows), "grand_total": grand})
















