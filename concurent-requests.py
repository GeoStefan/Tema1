from threading import Thread, Barrier
from random import randrange, choice
import requests
import json

barrier = Barrier(5)
failedConvert = 0
failedRocket = 0
failedQr =0

def getConvert():
    url = "http://localhost:8000/convert"
    amount = str(randrange(1, 10000))
    global failedConvert
    barrier.wait()
    try:
        result = requests.get(url,  params={"amount": amount})
        print('CONVERT  --- status code: ', result.status_code)
        if result.status_code != 200:
            failedConvert += 1
    except:
        failedConvert +=1

def getRocket():
    rocketId = choice(['falcon9', 'falconheavy', 'falcon1'])
    url = "http://localhost:8000/rocket/" + rocketId
    global failedRocket
    barrier.wait()
    try:
        result = requests.get(url)
        print('ROCKET  --- status code: ', result.status_code)
        if result.status_code != 200:
            failedRocket += 1
    except:
        failedRocket +=1

def getQr():
    url = "http://localhost:8000/qr"
    data = "name: Racheta, price: 10RON"
    size = "100x100"
    global failedQr
    barrier.wait()
    try:
        result = requests.post(url, json.dumps({"data": data, "size": size}))
        print('QR  --- status code: ', result.status_code)
        if result.status_code != 200:
            failedQr += 1
    except:
        failedQr +=1


if __name__ == "__main__":
    threads = []
    for i in range(0, 20):
        threads += [Thread(target=getConvert)]
        threads += [Thread(target=getRocket)]
        threads += [Thread(target=getQr)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("FAILED CONVERT: ", failedConvert)
    print("FAILED ROCKET: ", failedRocket)
    print("FAILED QR: ", failedQr)
