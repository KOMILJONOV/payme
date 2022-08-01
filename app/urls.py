from django.http import JsonResponse
from django.urls import path

from app.views import paymeView, home
from django.http.response import HttpResponse
def just_test(request):
    print(request.headers['Authorization'])
    return JsonResponse(request.headers)

urlpatterns = [
    path('payme', paymeView),
    path('', home),
    path('just',just_test)
]