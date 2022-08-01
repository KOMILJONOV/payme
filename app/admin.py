from django.contrib import admin

# Register your models here.
from .models import Transaction, Payment, Account

admin.site.register(Account)

admin.site.register(Payment)
admin.site.register(Transaction)