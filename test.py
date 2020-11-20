import csv

filename = '2020-11-20_11-32-27.csv'
##filename = 'test_2020-11-20_11-32-27.csv'
text = 'CityCard: код подтверждения карты:'

##with open (filename, 'r' ) as f:
##    reader = csv.reader(f)
##    for row in reader:
##        print (row)

phone_list = []
with open (filename, 'r') as f:
    reader = csv.DictReader(f, delimiter=';')
    pass
    for row in reader:
        if row['Идентификатор SMS'] == 'Всего SMS':
            break
        else:
            if text in row['Текст SMS']:
                phone_list.append(row['Номер телефона'])

