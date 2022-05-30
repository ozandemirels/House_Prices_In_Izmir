import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import date
import time

page = 1
house_list = []

def house_infos():
    for page in range(1, 500):
        if page == 1:
            url = 'https://www.hepsiemlak.com/izmir-satilik'
        elif page != 1:
            url = 'https://www.hepsiemlak.com/izmir-satilik?page=' + str(page)

        headers = {'User-Agent': 'my user agent(google)'}
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        home_divs = soup.find_all('div', class_='listing-item')

        for home_div in home_divs:
            home_price = home_div.find('div', class_='list-view-price').text.strip('TL').strip('EUR').strip('USD').strip()
            home_price_currency = home_div.find('span', class_='currency').text.strip()
            home_date = home_div.find('div', class_='list-view-date').text.strip()
            home_type = home_div.find('div', class_='left').text
            home_type = home_type[0:home_type.index(' ') - 1]
            home_numberofroom = home_div.find('span', class_='celly houseRoomCount').text.replace(' ', '')
            home_size = home_div.find('span', class_='celly squareMeter list-view-size').text.replace(' ', '').strip(' ')
            home_size = home_size[1:home_size.index('m') + 2]
            home_neighbourhood = home_div.find('div', class_='list-view-location').text.replace(' ', '')
            home_neighbourhood = home_neighbourhood[1:home_neighbourhood.index(',')]

            house_list.append([home_price, home_price_currency, home_date, home_type, home_numberofroom, home_size,home_neighbourhood])
        page += 1
        print(str(page) + '. sayfaya geçiliyor')

    workbook = Workbook()
    sheet = workbook.active

    for row in house_list:
        sheet.append(row)

    today = str(date.today())
    workbook.save(filename="C:/Users/ozan.demirel/Desktop/House_Prices/house_infos_in_izmir_" + today + ".xlsx")


while True:
    house_infos()
    time.sleep(60*60*24)



