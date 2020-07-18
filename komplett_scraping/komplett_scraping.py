#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging


def log_setup():
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level (lowest level)
    logger.setLevel(logging.DEBUG)

    # define file handler and set formatter
    file_handler = logging.FileHandler('logfile.log')
    formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)
    return logger


class Scraper:
    def __init__(self, category, URL):
        logger.debug(f'Initiating instance of class "{self.__class__.__name__}"')
        self.cat = category
        self.URL = URL
        self.URL_domain = self.URL.split('/')[2]
        logger.debug(f'Category: {self.cat}')
        logger.debug(f'URL: {self.URL}')
        try:
            self.get_info()
        except Exception as err:
            logger.error(f'Failed in method "{self.__class__.__name__}.get_info()": {err}', exc_info=True)

        try:
            self.save_record()
        except Exception as err:
            logger.error(f'Failed in method "{self.__class__.__name__}.save_record()": {err}', exc_info=True)

    def get_info(self): # gets overwritten
        self.name = ''
        self.price = ''
        self.date = ''
        self.part_num = ''

    def check_part_num(self):
        '''Checks if a product has a part number in the JSON-file, if it doesn't, it added to the JSON-file.'''
        changed = False
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            part_num_from_data = data[self.cat][self.name][self.URL_domain]['info']['part_num']
            if part_num_from_data == '':
                data[self.cat][self.name][self.URL_domain]['info']['part_num'] = self.part_num
                changed = True
            elif not self.part_num == part_num_from_data:
                data[self.cat][self.name][self.URL_domain]['info']['part_num_2'] = self.part_num
                changed = True
        if changed:
            with open('records.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

    def print_info(self):
        '''Print info about the product in the terminal.'''
        print(f'Kategori: {self.cat}\nNavn: {self.name}\nPris: {self.price} kr.\nDato: {self.date}\nFra domain: {self.URL_domain}\nProdukt nummer: {self.part_num}\n')

    def save_record(self):
        '''Save the price of the product in the JSON-file.'''
        logger.info('Saving record...')
        with open('records.json', 'r') as json_file:
            data = json.load(json_file)
            data[self.cat][self.name][self.URL_domain]["dates"][self.date] = {"price": self.price}
        with open('records.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info('Record saved')


def change_name(name):
    '''Change the name of the product, so if a similiar product is also being scraped, the similar products goes under the same name.'''
    if 'asus' in name and 'geforce' in name and 'rtx' in name and '2080' in name and 'ti' in name and 'rog' in name and 'strix' in name and 'oc' in name:
        name = 'asus geforce rtx 2080 ti rog strix oc'
    elif 'corsair' in name and 'mp600' in name and '1tb' in name and 'm.2' in name:
        name = 'corsair force mp600 1tb m.2'
    return name


class Komplett(Scraper):
    def get_info(self):
        logger.info('Getting response from URL...')
        self.response = requests.get(self.URL)
        logger.info('Got response from URL')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
        self.name = change_name(self.name)
        # find price
        self.price = self.html_soup.find('span', class_='product-price-now').text.strip(',-').replace('.', '')
        self.part_num = self.URL.split('/')[4]
        self.check_part_num()
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))


class Proshop(Scraper):
    def get_info(self):
        logger.info('Getting response from URL...')
        self.response = requests.get(self.URL)
        logger.info('Got response from URl')
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
        self.name = change_name(self.name)
        try:
            # find normal price
            self.price = self.html_soup.find('span', class_='site-currency-attention').text.split(',')[0].replace('.', '')
        except AttributeError:
            try:
                # find discount price
                self.price = self.html_soup.find('div', class_='site-currency-attention site-currency-campaign').text.split(',')[0].replace('.', '')
            except AttributeError:
                # if campaign is sold out (udsolgt)
                self.price = self.html_soup.find('div', class_='site-currency-attention').text.split(',')[0].replace('.', '')
        self.part_num = self.html_soup.find('small', class_='col-xs-12 text-center').strong.text
        self.check_part_num()
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))


class Computersalg(Scraper):
    def get_info(self):
        self.response = requests.get(self.URL)
        self.html_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.name = self.html_soup.find('h1', itemprop='name').text.lower()
        self.name = change_name(self.name)
        # find price
        self.price = self.html_soup.find('span', itemprop='price').text.strip().split(',')[0].replace('.', '')
        self.part_num = self.URL.split('/')[4]
        self.check_part_num()
        self.date = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))


def multiple_links(file_name):
    with open(f'{file_name}', 'r') as file:
        lines = file.readlines()

    count = 1
    for line in lines:
        print(f'Produkt {count}:')
        print(f'Link: {line.strip()}')
        #Product(line.strip()).print_info()
        count += 1


if __name__ == '__main__':
    logger = log_setup()
    Komplett('gpu', 'https://www.komplett.dk/product/1103205/hardware/pc-komponenter/grafikkort/asus-geforce-rtx-2080-ti-rog-strix-oc#')
    Komplett('ssd', 'https://www.komplett.dk/product/1133452/hardware/lagring/harddiskssd/ssd-m2/corsair-force-series-mp600-1tb-m2-ssd#')
    Proshop('gpu', 'https://www.proshop.dk/Grafikkort/ASUS-GeForce-RTX-2080-Ti-ROG-STRIX-OC-11GB-GDDR6-RAM-Grafikkort/2679518')
    Proshop('ssd', 'https://www.proshop.dk/SSD/Corsair-Force-MP600-NVMe-Gen4-M2-1TB/2779161')
