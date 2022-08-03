from django.contrib import admin

# Register your models here.
from .models import Transaction, Payment




class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['name', 'phone', 'usd_course', 'plan', 'amount']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction)