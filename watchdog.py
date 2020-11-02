import requests
import datetime, time

filename = 'log.log'
wait = 60

url = 'https://test.gorkarta.ru/RS.Loyalty.Service/RSLoyaltyService.svc?wsdl'
correct_answer = '<wsdl:message name="IRSLoyaltyService_Ping_InputMessage">'

def write_log(record, filename=filename):
    error_time = datetime.datetime.now().isoformat(sep = ' ', timespec ='seconds')
    row = f'{error_time}: {record} \n \n'
    with open (filename, 'a') as f:
        f.write(row)
    return


print('Старт')
while True:
    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        write_log(e)
    else:
        is_online = correct_answer in r.text
        if is_online:
            print(f'Время {time.ctime()}. Ответ сервера: {is_online}')
        else:
            write_log('Сервер доступен, но вернул неверный ответ')
        print(f'Задержка {wait} сек..')
    time.sleep(wait)