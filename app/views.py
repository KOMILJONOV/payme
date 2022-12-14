import base64
import json
import random
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from app.models import JustRequest, Payment
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
    # key = "RXxN?vmZ3#qM?DsXI%m9xhKzwsB2iR&kRWFr"
    
    def generate_pair_login_pass(self):
        return self.login + ":" + self.key
            


paymeView = PaymeView()




def home(request):
    new_user: Payment = Payment.objects.create(
        state=Payment.PAYMENT_ON_WAIT,
        phone="+998998704306"
    )
    return render(request, 'index.html', {
        'order_id': new_user.id
    })
import requests
def get_course():
    res = requests.get('https://nbu.uz/exchange-rates/json')
    if res.status_code == 200:
        for i in res.json():
            if i['code'] == "USD":
                return float(i['nbu_cell_price'])
    else:
        return get_course()

def register(request):
    res = request.body
    data = json.loads(res)
    usd_course = get_course()

    new_user: Payment = Payment.objects.create(
        name=data['name'],
        phone=data['number'],
        plan=data['plan'],
        usd_course=usd_course
    )
    print(
        new_user.usd_course,
        type(new_user.usd_course)
    )
    print(type(new_user.amount))
    return JsonResponse(
        {
            "ok": True,
            "data": {
                'id': new_user.id,
                'amount': new_user.amount
            }
        }
    )


def just_register(request):
    res = request.body
    data = json.loads(res)
    JustRequest.objects.create(
        **data
    )
    return JsonResponse({
        "ok": True
    })