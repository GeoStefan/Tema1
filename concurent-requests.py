from threading import Thread, Barrier
from random import randrange, choice
import requests
import json

barrier = Barrier(5)


def getConvert():
    url = "http://localhost:8000/convert"
    amount = str(randrange(1, 10000))
    barrier.wait()
    result = requests.get(url,  params={"amount": amount})
    print('CONVERT  --- status code: ', result.status_code)

def getRocket():
    rocketId = choice(['falcon9', 'falconheavy', 'falcon1'])
    url = "http://localhost:8000/rocket/" + rocketId
    barrier.wait()
    result = requests.get(url)
    print('ROCKET  --- status code: ', result.status_code)

def getQr():
    url = "http://localhost:8000/qr"
    data = "name: Racheta, price: 10RON"
    size = "100x100"
    barrier.wait()
    result = requests.post(url, json.dumps({"data": data, "size": size}))
    print('QR  --- status code: ', result.status_code)


if __name__ == "__main__":
    threads = []
    for i in range(0, 10):
        threads += [Thread(target=getConvert)]
        threads += [Thread(target=getRocket)]
        threads += [Thread(target=getQr)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
