from .base import BaseBehavior
from app.models import Transaction


class GetStatement(BaseBehavior):
    def execute(self):
        return Transaction.between(self.params['from'], self.params['to'])
