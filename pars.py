from bs4 import BeautifulSoup
import requests
import csv
import datetime
from datetime import datetime


# Отримання html коду для парсинга.
def get_html(url):
    r = requests.get(url)
    return r.text


#Записуємо графік автобусів ʼз Франківськаʼ в csv файл
def from_if_csv(data):
    with open('from_if.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([data['time'],
                         data['name']])


#Записуємо графік автобусів ʼз Тязеваʼ в csv файл
def from_tiaziv_csv(data):
    with open('from_tiaziv.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([data['time2'],
                         data['name']])


# Парсинг html коду
def get_data(html):

    # Додати в словник графік автобуса ʼТязівʼ
    tzv = {}
    n = 8
    while tzv.get('time') != '18.30' :
        if n == 11 or n == 12:
            n += 1
            continue
        tzv = {'time':(str(n) + '.30'),
               'name':'Тязів'}
        from_if_csv(tzv)
        n += 1

    tzv2 = {}
    n = 9
    while tzv2.get('time2') != '19.00':
        if n == 12 or n == 13:
            n += 1
            continue
        tzv2 = {'time2': (str(n) + '.00'),
               'name': 'Тязів'}
        from_tiaziv_csv(tzv2)
        n += 1

    # Парсинг сайту автостанції
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='tbl_afisha').find('tbody').find_all('tr')
#
    for tr in trs:
        tds = tr.find_all('td')
        time = tds[1].text.strip()

        time2 = tds[0].text.strip()

        # Віднімаємо від отриманого значення 20 хв
        time2 = time2.split('.')
        date_object = datetime.strptime(time2[0] + ':' + time2[1], '%H:%M')
        minut = datetime.strptime('20', '%M')
        time2 = (date_object - minut)
        time2 = (str(time2).split(':'))
        time2 = time2[0]+'.'+time2[1]

        name = tds[2].text.strip()

        banlist = ['Павлівка', 'Височанка', 'Рибне', 'Клузів', 'ІКлузів', 'Майдан', 'Тязів']

        # Пропуск непотрібних маршрутів
        if name in banlist:
            continue

        # Звичайний запис маршрутів
        else:
            dicti = {'time':time,
                     'name':name}

            dicti2 = {'time2':time2,
                     'name':name}

        from_if_csv(dicti)
        from_tiaziv_csv(dicti2)


def main():
    url = 'http://page.if.ua/article/20/'
    get_data(get_html(url))

#     d = get_data(get_html(url))
#     t = return_time((d), get_time())
#
#     return (final_result(t, d))

if __name__ == '__main__':
    main()
