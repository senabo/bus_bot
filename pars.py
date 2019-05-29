from bs4 import BeautifulSoup
import requests
import datetime
import pytz
from datetime import datetime


# Отримання актуального часу в UTC за Києвом.
def get_time():
    tzkiev = pytz.timezone('Europe/Kiev')
    utc = datetime.now(tzkiev).astimezone(tzkiev)
    now =  str(utc.time()).split(':')
    return (float(now[0]+'.'+now[1]))


# Отримання html коду для парсинга.
def get_html(url):
    r = requests.get(url)
    return r.text


# Парсинг html коду, отримання словника, де ключ-час відправлення, а значення-назва маршруту.
def get_data(html):
    # Додати в словник графік автобуса ʼТязівʼ
    dicti = {'6.45': 'Тязів', '7.15': 'Тязів'}
    n = 8
    while '19.30' not in [*dicti]:
        if n == 11 or n == 12:
            n += 1
            continue
        dicti[str(n) + '.30'] = 'Тязів'
        n += 1

    # Парсинг сайту автостанції
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='tbl_afisha').find('tbody').find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        time = tds[1].text.strip()
        name = tds[2].text.strip()

        banlist = ['Павлівка', 'Височанка', 'Рибне', 'Клузів', 'ІКлузів', 'Майдан', 'Тязів']

        # Пропуск непотрібних маршрутів
        if name in banlist:
            continue

        # Запис кількох маршрутів під один ключ, якщо час відправлення однаковий
        elif time in [*dicti]:
            l = dicti[time] + ' ◾️ ' + name
            dicti[time] = l

        # Звичайний запис маршрутів
        else:
            dicti[time] = name

    return dicti


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


numb = '5'

def get_number_bus(chat_id):

    f = open('numb_bus.txt')
    global numb
    for line in f:
        if str(chat_id) in line:
            numb = (line.split(',')[1])

        elif 'test' in line:
            numb = (line.split(',')[1])

    f.close()


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


# Фінальний результат
def shedule():
    url = 'http://page.if.ua/article/20/'
    d = get_data(get_html(url))
    t = return_time((d), get_time())

    return (final_result(t, d))


if __name__ == '__main__':
    shedule()
