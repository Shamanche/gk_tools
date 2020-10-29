import requests
import time
wait = 5
url = 'https://loyalty.gorkarta.ru/RS.Loyalty.Service/RSLoyaltyService.svc?wsdl'

correct_answer = '<wsdl:message name="IRSLoyaltyService_Ping_InputMessage">'

for i in range(5):
    r = requests.get(url, timeout=5)
##    print (r.status_code)
    is_online = correct_answer in r.text
    print(f'Время {time.ctime()}. Ответ сервера: {is_online}')
    print(f'Задержка {wait} сек..')
    time.sleep(wait)