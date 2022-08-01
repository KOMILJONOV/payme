from .base import BaseBehavior
from app.models import Transaction
from archive.exceptions import PaycomException
from app. models import PaymentHistory


class PerformTransaction(BaseBehavior):
    def execute(self):
        try:
            transaction:Transaction = Transaction.find_by_pk(self.params['id'])

            if transaction.is_created():
                if transaction.is_timeout() or transaction.is_cancelled_after_payment():
                    transaction.set_timed_out()
                    raise PaycomException("CANNOT_PERFORM_OPERATION")
            elif transaction.is_payed():
                return transaction

            if not transaction.is_cancelled() and not transaction.is_payed():
                transaction.set_payed()
                return transaction
            else:
                raise PaycomException("CANNOT_PERFORM_OPERATION")

        except Exception as e:
            print(e)
            raise PaycomException("CANNOT_PERFORM_OPERATION")
