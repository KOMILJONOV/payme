from .base import BaseBehavior
from app.models import Transaction, PaymentHistory


class CancelTransaction(BaseBehavior):
    def execute(self):
        print(self.params,"HHH")
        transaction:Transaction = Transaction.find_by_pk(self.params['id'])
        if transaction.state == Transaction.STATE_CANCELLED  or transaction.state == Transaction.STATE_CANCELLED_AFTER_PAYED:
            return transaction
        transaction.cancel(self.params['reason'])
        return transaction
