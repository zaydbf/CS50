from django.shortcuts import render
import datetime
from django.http import HttpResponse
# Create your views here.
# def index(request):
#     now = datetime.datetime.now()
#     day = now.day
#     month = now.month
#     year = now.year
#     if day == 15 and month == 4 and year == 2025:
#         return HttpResponse(request, "YES !")
#     else: 
#         return HttpResponse(request, "No!")    
def index(request):
    now = datetime.datetime.now()
    return render(request, "newyear/index.html", {
        "newyear": now.month == 1 and now.day == 1 
    })