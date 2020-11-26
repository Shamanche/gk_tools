import csv, datetime, keyring
import pymssql

stores = {} # хранит названия магазинов по StoreId

filename = '2020-11-26_10-11-53.csv'
text = 'CityCard: код подтверждения карты:'

def mssql_connect(): # добавить таймаут если сервер недоступен
    conn = pymssql.connect(
        server="loyalty.gorkarta.ru",
        database="RSLoyalty5",
        user=keyring.get_password('mssql', 'login'),
        password=keyring.get_password('mssql', 'user'),
        port=int(keyring.get_password('mssql', 'port')),
        login_timeout=29) # heroku имеет ограничение на таймаут ответа 30 с.
    return conn

## Возвращает список магазинов в которых совершались покупки в дату sms_date
def get_store_id(conn, sms_date, phone):
    curent_sms_date = sms_date.strftime('%Y-%m-%d')
    next_sms_date = (sms_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    sql_request = '''
        set dateformat ymd
        select distinct Transactions.StoreID
        from Transactions, DiscountCards, Accounts, CustomerPhones
        where Transactions.TransactionTime between '{}' and '{}'
        	and CustomerPhones.CustomerID = Accounts.CustomerID
        	and Accounts.AccountID = DiscountCards.AccountID
        	and DiscountCards.DiscountCardID = Transactions.DiscountCardID
        	and CustomerPhones.Phone = '{}'
            '''.format(curent_sms_date, next_sms_date, phone)
##    print(sql_request)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

def test_get_store_id(conn):
    sql_request = '''
        set dateformat ymd
        select distinct Transactions.StoreID
        from Transactions, DiscountCards, Accounts, CustomerPhones
        where Transactions.TransactionTime between '2020-01-20' and '2020-02-23'
        	and CustomerPhones.CustomerID = Accounts.CustomerID
        	and Accounts.AccountID = DiscountCards.AccountID
        	and DiscountCards.DiscountCardID = Transactions.DiscountCardID
        	and CustomerPhones.Phone = '79183195479'
            '''
##    print(sql_request)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows


def parse_sms_csv(filename):
    phone_list = []
    with open (filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Идентификатор SMS'] == 'Всего SMS': #признак заверщения данных
                break
            else:
                if text in row['Текст SMS']:
                    data_dict = {}
                    data_dict['id'] = row['Идентификатор SMS']
                    data_dict['phone'] = row['Номер телефона']
                    datetime_str = row['Время отправки SMS']
                    data_dict['date'] = datetime.datetime.strptime(datetime_str,
                                                            '%Y-%m-%d %H:%M:%S')
                    data_dict['price'] = row['Цена'].replace('.',',')
                    phone_list.append(data_dict)
    return phone_list

# возвращает название магазина по номеру, и сохраняет в stores{}
def get_store_name(conn, store_id):
    if stores.get(store_id, 'Empty') == 'Empty':
            sql_request = '''
                select Name from Stores where StoreID = {}
                '''.format(store_id)
##            print(sql_request)
            cursor = conn.cursor()
            cursor.execute(sql_request)
            row = cursor.fetchone()
            stores[store_id] = row[0]
    return stores.get(store_id, 'Error store_id')

def save_file_csv(conn, data_dict, filename):
    if data_dict:
        fieldnames = [i for i in data_dict[0].keys()]
    else:
        print ('Не найдены заголовки таблиц данные!')
        fieldnames = []

    with open (filename, 'w', newline='' ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for elem in data_dict:
            if elem['store']:
                store_id_list = elem['store']
                for store_id in store_id_list:
                    elem['store'] = get_store_name(conn, store_id)
                    writer.writerow(elem)
            else:
                elem['store'] = '+++Активность не найдена+++'
                writer.writerow(elem)
    print('Файл {} создан'.format(filename))
    return

parsed_data = parse_sms_csv(filename)
conn = mssql_connect()

for num, elem in enumerate(parsed_data):
    store_id_list = get_store_id(conn, elem['date'], elem['phone'])
##    store_id_list = test_get_store_id(conn)
    parsed_data[num]['store'] = [i[0] for i in store_id_list]

save_file_csv(conn, parsed_data, 'result.csv')
conn.close()









