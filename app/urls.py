from django.http import JsonResponse
from django.urls import path

from app.views import paymeView, home,register, just_register


urlpatterns = [
    path('payme', paymeView),
    path('', home),
    path('register', register),
    path('just_register', just_register)
]