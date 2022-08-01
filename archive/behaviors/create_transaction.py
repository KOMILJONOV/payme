from .base import BaseBehavior
from app.models import PaymentHistory, Transaction
from archive.exceptions import PaycomException
from .check_perform_transaction import CheckPerformTransaction
from archive.utils import time_now_in_ms


class CreateTransaction(BaseBehavior):
    def execute(self):

        try:
            transaction: Transaction = Transaction.find_by_pk(
                self.params['id'])
            if not transaction.is_created():
                raise PaycomException("CANNOT_PERFORM_OPERATION")
            if transaction.is_timeout():
                transaction.set_timed_out()
                raise PaycomException("CANNOT_PERFORM_OPERATION")

            return transaction

        except Exception as e:
            print(e)

        check_perform = CheckPerformTransaction(self.params)
        check_perform.execute()

        user: Transaction = Transaction.objects.filter(
            account=self.params['account']['login']).first()
        if user and user.state == 1:
            return {
                "ok": False,
                "error": {
                    "code": -31099,
                    "message": "salom"
                }
            }

        transaction_dict = {
            "time": self.params['time'],
            "transaction_id": self.params['id'],
            "account": self.params['account']['login'],
            "amount": self.params['amount'],
            "create_time": time_now_in_ms(),
            "state": Transaction.STATE_CREATED,
            "transaction": self.params['id'],
        }
        return Transaction.objects.create(**transaction_dict)
