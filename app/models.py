from django.db import models
from archive.exceptions import PaycomException

import time


def sum2coins(amount):
    return amount * 100


def coin2sums(amount):
    return amount / 100


def time_now_in_ms():
    return int(time.time() * 1000)


# Create your models here.
# class PaymentHistory(models.Model):
#     PAYMENT_ON_WAIT = 1
#     PAYMENT_IS_PAYED = 2
#     PAYMENT_CANCELLED = -1

#     account = models.IntegerField(blank=False)
#     state = models.SmallIntegerField(blank=False)
#     amount = models.IntegerField(blank=False)
#     phone = models.CharField(max_length=15, blank=False)




    
        



#     def on_wait(self):
#         return self.state == self.PAYMENT_ON_WAIT

#     def is_payed(self):
        
#         return self.state == self.PAYMENT_IS_PAYED

#     def is_cancelled(self):
#         return self.state == self.PAYMENT_CANCELLED

#     def set_payed(self):
#         self.state = self.PAYMENT_IS_PAYED
#         self.save()

#     def cancel(self):
#         self.state = self.PAYMENT_CANCELLED
#         self.save()

#     @staticmethod
#     def find_by_pk(pk):
#         print(pk)
#         try:
#             history = PaymentHistory.objects.get(account=pk)
#             return history
#         except PaymentHistory.DoesNotExist as e:
#             raise PaycomException("ORDER_NOT_FOUND")

# class Transaction(models.Model):
#     TIMEOUT_LIMIT = 43200000

#     STATE_CREATED = 1
#     STATE_PAYED = 2
#     STATE_CANCELLED = -1
#     STATE_CANCELLED_AFTER_PAYED = -2

#     REASON_USER_NOT_FOUND_ERROR = 1
#     REASON_DEBIT_OPERATION_ERROR = 2
#     REASON_EXECUTION_ERROR = 3
#     REASON_TIMEOUT_CANCEL_ERROR = 4
#     REASON_REFUND = 5
#     REASON_UNDEFINED_ERROR = 6

#     # paycom transaction id
#     transaction_id = models.CharField(max_length=25, blank=False)
#     # paycom transaction time
#     time = models.CharField(max_length=13, blank=False)

#     amount = models.IntegerField(blank=False)
#     account = models.CharField(blank=False, max_length=255)

#     create_time = models.BigIntegerField(blank=True, default=0)
#     perform_time = models.BigIntegerField(blank=True, default=0)
#     cancel_time = models.BigIntegerField(blank=True, default=0)

#     transaction = models.CharField(blank=False, max_length=25)
#     state = models.SmallIntegerField(blank=False)
#     reason = models.SmallIntegerField(blank=True, default=0)
#     receivers = models.CharField(max_length=500, blank=False)

#     def is_created(self):
#         return self.state == self.STATE_CREATED

#     def is_payed(self):
#         return self.state == self.STATE_PAYED

#     def is_cancelled(self):
#         return self.state == self.STATE_CANCELLED

#     def is_cancelled_after_payment(self):
#         return self.state == self.STATE_CANCELLED_AFTER_PAYED

#     def is_timeout(self):
#         return time_now_in_ms() - self.create_time > self.TIMEOUT_LIMIT

#     def set_timed_out(self):
#         self.reason = self.REASON_TIMEOUT_CANCEL_ERROR
#         self.state = self.STATE_CANCELLED
#         return self.save()

#     def cancel(self, reason):
#         if self.is_payed():
#             self.state = self.STATE_CANCELLED_AFTER_PAYED
#         elif self.is_created():
#             self.state = self.STATE_CANCELLED
#         self.cancel_time = time_now_in_ms()
#         self.reason = reason
#         return self.save()

#     def set_payed(self):
#         self.state = Transaction.STATE_PAYED
#         self.perform_time = time_now_in_ms()
#         self.save()

#     @classmethod
#     def between(cls, from_date, to_date):
#         return Transaction.objects.filter(create_time__gte=from_date, create_time__lte=to_date)

#     @staticmethod
#     def find_by_pk(pk):
#         try:
#             transaction = Transaction.objects.get(transaction=pk)
#             return transaction
#         except Transaction.DoesNotExist as e:
#             raise PaycomException("TRANSACTION_NOT_FOUND")



class Account(models.Model):
    pass

class Payment(models.Model):
    PAYMENT_ON_WAIT = 1
    PAYMENT_IS_PAYED = 2
    PAYMENT_CANCELLED = -1

    state = models.SmallIntegerField(blank=False, choices=[
        (1, "On wait"),
        (2, "Payed"),
        (-1, "Cancelled"),
    ])
    amount = models.IntegerField(blank=False)
    phone = models.CharField(max_length=15, blank=False)


class Transaction(models.Model):
    id: int

    STATE_CREATED = 1
    STATE_PAYED = 2
    STATE_CANCELLED = -1
    STATE_CANCELLED_AFTER_PAYED = -2

    REASON_USER_NOT_FOUND_ERROR = 1
    REASON_DEBIT_OPERATION_ERROR = 2
    REASON_EXECUTION_ERROR = 3
    REASON_TIMEOUT_CANCEL_ERROR = 4
    REASON_REFUND = 5
    REASON_UNDEFINED_ERROR = 6





    trans_id = models.CharField(max_length=50)
    time = models.CharField(max_length=13)

    amount = models.IntegerField(default=0)
    account = models.IntegerField(default=0)


    create_time = models.BigIntegerField(default=0)
    perform_time = models.BigIntegerField(default=0)
    cancel_time = models.BigIntegerField(default=0)

    transaction = models.CharField(max_length=50)
    state = models.SmallIntegerField(choices=[
        (1, "Created"),
        (2, "Payed"),
        (-1, "Cancelled"),
        (-2, "Cancelled after payed"),
    ])
    reason = models.SmallIntegerField(default=0, choices=[
        (1, "User not found error"),
        (2, "Debit operation error"),
        (3, "Execution error"),
        (4, "Timeout cancel error"),
        (5, "Refund"),
        (6, "Undefined error"),
    ])

    receivers = models.CharField(max_length=500)
    
    def set_payed(self):
        self.state = self.STATE_PAYED
        self.perform_time = time_now_in_ms()
        self.save()
    
    def cancel(self, reason: int):
        if self.state == self.STATE_CREATED or self.state == self.STATE_PAYED:
            self.cancel_time = time_now_in_ms()

        if self.state == self.STATE_CREATED:
            self.state = self.STATE_CANCELLED

        elif self.state == self.STATE_PAYED:
            self.state = self.STATE_CANCELLED_AFTER_PAYED

        self.reason = reason
        self.save()