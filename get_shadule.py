import csv
import datetime
import pytz
from datetime import datetime


# Отримання актуального часу в UTC за Києвом.
def get_time():
    tzkiev = pytz.timezone('Europe/Kiev')
    utc = datetime.now(tzkiev).astimezone(tzkiev)
    now =  str(utc.time()).split(':')
    return (float(now[0]+'.'+now[1]))


# Створення словника з розкладом ʼз Франківськаʼ, де ключ - година, а значення - автобус
def dict_from_if():

    dict_if = {}

    # Дані беремо з готового csv файла
    with open('from_if.csv') as f:
        fieldnames = ['time', 'name']
        reader = csv.DictReader(f, fieldnames= fieldnames)

        for row in reader:

            time = row['time']
            name = row['name']

            # Запис кількох маршрутів під один ключ, якщо час відправлення однаковий
            if time in [*dict_if]:
                l = dict_if[time] + ' ◾️ ' + name
                dict_if[time] = l
            # Звичайний запис
            else:
                dict_if[time] = name

        return dict_if


# Створення словника з розкладом ʼз Тязеваʼ, де ключ - година, а значення - автобус
def dict_from_tiaziv():
    dict_t = {}

    # Дані беремо з готового csv файла
    with open('from_tiaziv.csv') as f:
        fieldnames = ['time', 'name']
        reader = csv.DictReader(f, fieldnames=fieldnames)

        for row in reader:

            time = row['time']
            name = row['name']

            # Запис кількох маршрутів під один ключ, якщо час відправлення однаковий
            if time in [*dict_t]:
                l = dict_t[time] + ' ◾️ ' + name
                dict_t[time] = l
            # Звичайний запис
            else:
                dict_t[time] = name

        return dict_t


# Отримання кількості автобусів для відображення.
def number_bus(n, chat_id):
    f = open('numb_bus.txt')
    for line in f:
        if str(chat_id) in line:
            f = open('numb_bus.txt').read()
            fi = f.replace(line, '')

            f = open('numb_bus.txt', 'w')
            f.write(fi)
            f.close()

    f = open('numb_bus.txt', 'a')
    f.write(str(chat_id) + ',' + n + '\n')
    f.close()

numb = '8'

def get_number_bus(chat_id):

    f = open('numb_bus.txt')
    global numb
    for line in f:
        if str(chat_id) in line:
            numb = (line.split(',')[1])

        elif 'test' in line:
            numb = (line.split(',')[1])

    f.close()


def last_message(m,chat_id):

    f = open('last_message.txt')
    for line in f:
        if str(chat_id) in line:
            f = open('last_message.txt').read()
            fi = f.replace(line, '')

            f = open('last_message.txt', 'w')
            f.write(fi)
            f.close()

    f = open('last_message.txt', 'a')
    f.write(str(chat_id) + ',' + str(m) + '\n')
    f.close()


def get_last_mes(chat_id):
    f = open('last_message.txt')

    for line in f:
        if str(chat_id) in line:
            mes = (line.split(',')[1])

        elif 'test' in line:
            mes = (line.split(',')[1])

    f.close()

    return  mes



# Отримання автобусів, відповідно до заданого часу.
def return_time(dicti, time):
    # Створення списку з часом відправлення + додаємо свій час
    list_time = []

    for i in [*dicti]:
        list_time.append(float(i))

    list_time.append(time)

    # Сортування списка, отримання індекса нашого часу
    list_time.sort()
    index = list_time.index(time)

    # Виключаємо автобуси які їдуть в ту саму хвилину коли робимо запит
    if format(time,'.2f') in [*dicti]:
        index+=1

    # Отримання списку потрібних автобусів
    result = []
    global numb
    try:
        list_time[index + 1] # Перевіряємо чи час запиту пізніший за час останнього маршрута

        a = list_time[(index + 1): (index + int(numb)+1)]

        for i in a:
            result.append(format(i, '.2f'))
        return result

    except IndexError:
        a = list_time[0: int(numb)]

        for i in a:
            result.append(format(i, '.2f'))
        return result


# Форматування списка з маршрутами для відправлення користувачу
def final_result(t, d):
    text = ''
    t.reverse()
    for i in t:
        text = ('🕖  ' + i + ' ➖ ' + d[i]) + '\n\n' + text
    return text


def in_tiaziv():
    d = dict_from_if()
    t = return_time((d), get_time())
    return (final_result(t, d))


def in_frankivsk():
    d = dict_from_tiaziv()
    t = return_time((d), get_time())
    return ('⚠️ Розклад неточний \n\n'+final_result(t, d))
