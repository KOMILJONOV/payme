# Merchant ID - 621e19c42590be2d78408142
# KEY - o?2veaMRDqzdqq&iIREA7qe&i4kyZrEiSUGJ
# TEST KEY - RXxN?vmZ3#qM?DsXI%m9xhKzwsB2iR&kRWFr



import requests
def get_course():
    res = requests.get('https://nbu.uz/exchange-rates/json')
    if res.status_code == 200:
        for i in res.json():
            if i['code'] == "USD":
                return i['nbu_cell_price']
    else:
        return get_course()

print(
    get_course()
)

for _ in range(10):
    print(
        get_course()
    )