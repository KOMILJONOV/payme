import base64
import json
import os
import random
from time import sleep
from django.http import JsonResponse
from django.shortcuts import render
from app.models import Payment
from paycom import Paycom




class Request:
    method: str
    body: bytes
    META: "dict[str, str]"


class PaymeView:
    def __init__(self):
        pass
    
    def __call__(self,request:Request):
        self.data = json.loads(request.body)
        auth = self.authentication(request)
        if auth:
            self.paycom = Paycom(self.data)
            res = self.paycom.launch()
            print(res)
            response = {
                'jsonrpc': '2.0',
                'id': self.data['id'],
                'result': res['result']
            }  if res['ok'] else {
                'jsonrpc': '2.0',
                'id': self.data['id'],
                'error': res['error']
            }
            response['auth'] = auth
            return JsonResponse(response)
        else:
            return JsonResponse(
                {
                    'jsonrpc': '2.0',
                    'id': self.data['id'],
                    'error': {
                        'code': -32504,
                        'message': 'Authorization required'
                    }
                }
            )
    

    def authentication(self,request:Request):
        if 'Authorization' not in request.headers:
            return False

        if 'HTTP_AUTHORIZATION' not in request.META:
            return False
        auth = request.META['HTTP_AUTHORIZATION']
        password = str(auth.replace("Basic", "")).strip()
        decoded = base64.b64decode(password)
        if self.generate_pair_login_pass().encode() != decoded:
            return False
        return True

    login = "Paycom"
    key = "o?2veaMRDqzdqq&iIREA7qe&i4kyZrEiSUGJ"
    
    def generate_pair_login_pass(self):
        return self.login + ":" + self.key
            


paymeView = PaymeView()






# class Payme:

#     login = "Paycom"
#     key = 'o?2veaMRDqzdqq&iIREA7qe&i4kyZrEiSUGJ'

#     def __call__(self, request):
#         data = json.loads(request.body)
#         self.launch(request, data)

    


#     def auth(self, request, data):
#         if 'HTTP_AUTHORIZATION' not in request.META:
#             return {
#                 "ok": False,
#                 "error": "UNAUTHENTICATED"
#             }
    
#         basic = self.request.META['HTTP_AUTHORIZATION']
#         password = str(basic.replace("Basic", "")).strip()
#         decoded = base64.b64decode(password)
#         if self.generate_pair_login_pass().encode() != decoded:
#             return {
#                 "ok": False,
#                 "error": "UNAUTHENTICATED"
#             }
#         return True
    

#     def generate_pair_login_pass(self):
#         return self.login + ":" + self.key
    

#     def launch(self, request, data):
#         self.auth(request, data)
#         if data['method'] == "CheckPerformTransaction":
#             pass











# from archive.exceptions import PaycomException
# from archive.paycom import Paycom
# from paycom import Paycom, PaycomException

# Create your views here.
# def payme(request):
#     data = json.loads(request.body)
#     print(data)
#     return JsonResponse(
#         {
#             "jsonrpc": "2.0",
#             "result": 1,
#             "id": data['id']
#         }
#     )


# def payme(request):
#     data = json.loads(request.body)
#     print(data)
#     paycom = Paycom(request)
    
#     try:
#         response = paycom.launch()
#     except PaycomException as e:
#         response = {
#             "result": "",
#             "error": {
#                 "code": e.ERRORS_CODES[e.code],
#                 "message": e.message,
#                 "data": ""
#             }
#         }

#         if 'id' in paycom.params:
#             response['id'] = paycom.params['id']
#     return JsonResponse(response)



def home(request):
    login = random.randint(1, 1000000)
    Payment.objects.create(
        account=login,
        state=Payment.PAYMENT_ON_WAIT,
        amount=5000,
        phone="+998998704306"
    )
    return render(request, 'index.html', {
        'order_id': login
    })
