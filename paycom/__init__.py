import base64
from app.models import Payment, Transaction


CHECK_PERFORM_TRANSACTION = 'CheckPerformTransaction'
CREATE_TRANSACTION = 'CreateTransaction'
PERFORM_TRANSACTION = 'PerformTransaction'
CANCEL_TRANSACTION = 'CancelTransaction'
CHECK_TRANSACTION = 'CheckTransaction'
GET_STATEMENT = 'GetStatement'


class ParamsAccount:
    id: int
    login: str

    def __init__(self, account: dict):
        self.login = account.get('login')


class ParamsParams:
    amount: int
    account: ParamsAccount
    time: int
    reason: int
    id: str

    def __init__(self, params: dict):
        self.amount = params.get('amount')
        self.account = ParamsAccount(params['account']) if 'account' in params else None
        self.time = params.get('time')
        self.id = params.get('id')
        self.reason = params.get('reason')



class Params:
    id: int
    jsonrpc: str = "2.0"
    method: str
    params: ParamsParams

    def __init__(self, data) -> None:
        self.id = data['id']
        self.data = data
        self.method = data['method']
        self.params: ParamsParams = ParamsParams(data['params'])

    def __str__(self) -> str:
        return str(self.data)


class Paycom:
    def __init__(self, data) -> None:
        self.data = data
        self.params = Params(data)
    

    def authentication(self,request):
        if 'Authorization' not in  request.headers:
            return {
                "ok": False,
                "error": {
                    "code": -32504,
                    "message": "Authorization required"
                }
            }
        if 'HTTP_AUTHORIZATION' not in request.META:
            return {
                "ok": False,
                "error": {
                    "code": "AUTHORIZATION_REQUIRED",
                    "message": "Authorization required"
                }
            }
        auth = request.META['HTTP_AUTHORIZATION']
        password = str(auth.replace("Basic", "")).strip()
        decoded = base64.b64decode(password)
        if self.generate_pair_login_pass().encode() != decoded:
            return False
        return True
    login = "Paycom"
    key = "o?2veaMRDqzdqq&iIREA7qe&i4kyZrEiSUGJ"
    # key = "RXxN?vmZ3#qM?DsXI%m9xhKzwsB2iR&kRWFr"
    
    def generate_pair_login_pass(self):
        return self.login + ":" + self.key

    def launch(self):
        if self.params.method == CHECK_PERFORM_TRANSACTION:
            res = self.check_perform_transaction()
            print(res)
            return res
        elif self.params.method == CREATE_TRANSACTION:
            return self.create_transaction()
        elif self.params.method == PERFORM_TRANSACTION:
            return self.perform_transaction()
        elif self.params.method == CANCEL_TRANSACTION:
            return self.cancel_transaction()
        elif self.params.method == CHECK_TRANSACTION:
            return self.check_transaction()

        print("sdfsdf")
        
        return 1

    def check_perform_transaction(self):
        if not self.params.params.account.login:
            return {
                "ok": False,
                "error": {
                    "code": -32504,
                    "message":{
                        "uz": "Foydalanuvchi topilmadi.",
                        "ru": "Пользователь не найден.",
                        "en": "User not found."
                    }
                }
            }

        pay: Payment = Payment.objects.filter(
            id=self.params.params.account.login
        ).first()
        if not pay:
            return {
                "ok": False,
                "error": {
                    "code": -31099,
                    "message": {
                        "uz": "Foydalanuvchi topilmadi.",
                        "ru": "Пользователь не найден.",
                        "en": "User not found."
                    }
                }
            }
        
        

        if self.params.params.amount != pay.amount:
            return {
                "ok": False,
                "error": {
                    "code": -31001,
                    "message": "salom2"
                }
            }
        
        if pay.state in (
            Payment.PAYMENT_IS_PAYED,
            Payment.PAYMENT_CANCELLED
        ):
            return {
                "ok": False,
                "error": {
                    "code": -31099,
                    "message": {
                        "uz":"To'lov amalga oshirib bo'lingan!" if pay.state == Payment.PAYMENT_IS_PAYED else "Kechirasiz to'lov bekor qilingan.",
                        "ru":"Оплата завершена!" if pay.state == Payment.PAYMENT_IS_PAYED else "Извините, платеж отменен.",
                        "en":"Payment completed!" if pay.state == Payment.PAYMENT_IS_PAYED else "Sorry, the payment has been cancelled.",
                    } 
                }
            }
        
        


        return {
            "ok": True,
            "result": {
                "allow": True,
                "id": self.params.params.id
            }
        }

    def create_transaction(self):
        check = self.check_perform_transaction()

        if not check['ok']:
            return check


        # if check['ok']:
        check_exists:Transaction = Transaction.objects.filter(
            trans_id=self.params.params.id
        ).first()

        if check_exists:
            return {
            "ok": True,
            "result": {
                "transaction": str(check_exists.id),
                "create_time": check_exists.create_time,
                "state": check_exists.state
            }
        }

        if not self.params.params.account.login:
            return {
                "ok": False,
                "error": {
                    "code": -32504,
                    "message": {
                        "uz": "Foydalanuvchi topilmadi.",
                        "ru": "Пользователь не найден.",
                        "en": "User not found."
                    }
                }
            }
        user: Transaction = Transaction.objects.filter(account=self.params.params.account.login).first()
        if user:
                    return {
                        "ok": False,
                        "error":{
                            "code": -31099,
                            "message": "salom3"
                        }
                    }


        transaction_data = {
                "time": self.params.params.time,
                "trans_id": self.params.params.id,
                "account": self.params.params.account.login,
                "amount": self.params.params.amount,
                "state": Transaction.STATE_CREATED,
                "transaction": self.params.params.id,
                "create_time": self.params.params.time,
        }

        new_transaction: Transaction = Transaction.objects.create(
            **transaction_data)

        return {
            "ok": True,
            "result": {
                "transaction": str(new_transaction.id),
                "create_time": new_transaction.create_time,
                "state": new_transaction.state
            }
        }
        # else:
        #     return check


    def perform_transaction(self):
        transaction: Transaction = Transaction.objects.filter(
            trans_id=self.params.params.id
        ).first()

        if transaction:
            if transaction.state == Transaction.STATE_CREATED:
                transaction.set_payed()
                return {
                    "ok": True,
                    "result": {
                        "transaction": str(transaction.id),
                        "perform_time": transaction.perform_time,
                        "state": transaction.state
                    }
                }
            elif transaction.state == Transaction.STATE_PAYED:
                return {
                    "ok": True,
                    "result": {
                        "transaction": str(transaction.id),
                        "perform_time": transaction.perform_time,
                        "state": transaction.state
                    }
                }
            elif transaction.state == Transaction.STATE_CANCELLED or transaction.state == Transaction.STATE_CANCELLED_AFTER_PAYED:
                return {
                    "ok": False,
                    "error": {
                        "code": -31008,
                        "message": "salom"
                    }
                }
        else:
            return {
                "ok": False,
                "error": {
                    "code": -31003,
                    "message": "salom"
                }
            }
    

    def cancel_transaction(self):
        transaction: Transaction = Transaction.objects.filter(
            trans_id=self.params.params.id
        ).first()
        if transaction:
            transaction.cancel(self.params.params.reason)
            return {
                "ok": True,
                "result": {
                    "transaction": str(transaction.id),
                    "cancel_time": transaction.cancel_time,
                    "state": transaction.state,
                }
            }
            pass
        else:
            pass
    

    def check_transaction(self):

        transaction: Transaction = Transaction.objects.filter(
            trans_id = self.params.params.id
        ).first()

        if transaction:
            return {
                "ok": True,
                "result": {
                    "create_time": transaction.create_time,
                    "perform_time": transaction.perform_time,
                    "cancel_time": transaction.cancel_time,
                    "transaction": str(transaction.id),
                    "state": transaction.state,
                    "reason": transaction.reason if transaction.reason else None
                }
            }
        else:
            return {
                "ok": False,
                "error": {
                    "code": -31008,
                    "message": "salom"
                }
            }