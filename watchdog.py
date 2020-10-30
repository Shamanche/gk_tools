import requests
import time
wait = 2
url = 'https://test.gorkarta.ru/RS.Loyalty.Service/RSLoyaltyService.svc?wsdl'

correct_answer = '<wsdl:message name="IRSLoyaltyService_Ping_InputMessage">'
print('Старт')
for i in range(30):
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.ConnectTimeout as e:
        print ('Исключение: ', e)
        print( '+++ TimeoutError +++')
    else:
        is_online = correct_answer in r.text
        print(f'Время {time.ctime()}. Ответ сервера: {is_online}')
        print(f'Задержка {wait} сек..')
        time.sleep(wait)