import csv
import pyodbc
import datetime
from sys import argv

title = 'Кроп-Пиво дарит бонусы ко дню рождения'
message = 'Вы получили 150 бонусов ко дню рождения от сети фирменных магазинов «Кроп-Пиво». Списать бонусы можно за 3 дня до, в день или 3 дня после дня рождения.'

if len(argv) == 1:
    filename = 'messages.csv'
else:
    filename = argv[1]

print ('filename: ', filename)

current_date = datetime .datetime.now()
# берем вчера для тестирования
next_day_date = current_date.replace(day = current_date.day + 1)
#print(current_date)

driver = 'DRIVER={ODBC Driver 17 for SQl Server}'
server = 'SERVER=localhost'
port = 'PORT=1433'
db = 'DATABASE=RSLoyalty5'
user = 'UID=sa'
pw = 'PWD=Hymp1122'
conn_str = ';'.join([driver, server, port, db, user, pw])
print(conn_str)

script = """
    SELECT distinct StringValue  FROM MailingToCustomers, CustomerPropertyValues
    where [MailingToCustomers].CustomerID=CustomerPropertyValues.customerid
    and DateAdded > '{}' and DateAdded < '{}'
    and ChequeID is null
    and propertyid = 5
    and MailingID=1096
    and StringValue is not null
    """.format(current_date.strftime('%Y-%d-%m'),
                                            next_day_date.strftime('%Y-%d-%m'))


print(script)

##script = '''
##    SELECT TOP 100 *
##    FROM [RSLoyalty5].[dbo].[Customers]
##        '''

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute(script)
sql_response = cursor.fetchall()

# убираем '+' и устанавливаем первой цифрой '7'
phone_list = [ '7' + i[0].strip('+')[1:] for i in sql_response]


cnum = ''
##phone_list = [
##    '79278642340',
##    '79176542689',
##    '79083061932']

final_list = []

first_line = ['cnum', 'phone', 'title', 'text']
final_list.append(first_line)
for phone in phone_list:
    row = [cnum, phone, title, message]
    final_list.append(row)

#csv.register_dialect('excel', delimiter=';')
with open (filename, 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=';' )
    for line in final_list:
        writer.writerow(line)


