from django.db import models

import time


def sum2coins(amount):
    return amount * 100


def coin2sums(amount):
    return amount / 100


def time_now_in_ms():
    return int(time.time() * 1000)



class Payment(models.Model):
    id: int
    PAYMENT_ON_WAIT = 1
    PAYMENT_IS_PAYED = 2
    PAYMENT_CANCELLED = -1


    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=15, blank=False)
    usd_course = models.FloatField(default=11015.0)
    plan = models.IntegerField(choices=[
        (1, 'Standart'),
        (2, "Premium"),
        (3, "VIP")
    ], default=0)



    state = models.SmallIntegerField(blank=False, choices=[
        (1, "On wait"),
        (2, "Payed"),
        (-1, "Cancelled"),
    ], default=1)


    @property
    def amount(self):
        return (
            179 if self.plan == 1 else (
                229 if self.plan == 2 else 399
            )
        ) * self.usd_course
        


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
        Payment.objects.filter(id=self.account).update(state=Payment.PAYMENT_IS_PAYED)
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








class JustRequest(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=15, blank=False)
    plan = models.IntegerField(choices=[
        (1, 'Standart'),
        (2, "Premium"),
        (3, "VIP")
    ], default=0)