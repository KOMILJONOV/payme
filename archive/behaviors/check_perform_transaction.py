from .base import BaseBehavior
from archive.exceptions import PaycomException
from app.models import PaymentHistory

class CheckPerformTransaction(BaseBehavior):
    def execute(self):
        if 'login' not in self.params['account']:
            raise PaycomException("ORDER_NOT_FOUND")
        pay = PaymentHistory.find_by_pk(self.params['account']['login'])
        

        # if not user.can_access():
        #     raise PaycomException("CANNOT_PERFORM_OPERATION")

        if self.params['amount'] != pay.amount:
            raise PaycomException("AMOUNTS_NOT_EQUALS")
        return True
    