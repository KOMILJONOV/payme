from django.http import JsonResponse
from django.urls import path

from app.views import paymeView, home,register


urlpatterns = [
    path('payme', paymeView),
    path('', home),
    path('register', register)
]