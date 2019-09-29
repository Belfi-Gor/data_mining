from bs4 import BeautifulSoup
#import lxml
import requests
import json
import time
import random
import re
from pymongo import MongoClient


class findJob:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'

    def __init__(self):  # , spec, page_start, pages, sleep_min, sleep_max):
        self.spec_list = False
        self.spec_to_parse = False
        self.parse_sleep_min = 10
        self.parse_sleep_max = 20
        self.is_hh = False
        self.is_sj = False
        self.hh_page_start = 0
        self.sj_page_start = 0
        self.sleep_min = 1
        self.sleep_max = 5
        self.vak_array = []

    def get_init_data(self):
        self.chooose_spec()
        self.is_hh = int(input("Парсить HH? 0 - нет; 1 - да"))
        if self.is_hh == 1:
            self.hh_page_start = int(input("Номер страницы с которой начать парсить HH. 0 - с первой страницы"))
            if self.hh_page_start < 0: self.hh_page_to_parse = 0
            self.hh_page_to_parse = int(input("Сколько страниц парсить. Минимум 1"))
            if self.hh_page_to_parse < 1: self.hh_page_to_parse = 1
        else:
            self.is_hh = 0

        self.is_sj = int(input("Парсить SJ? 0 - нет; 1 - да"))
        if self.is_sj == 1:
            self.sj_page_start = int(input("Номер страницы с которой начать парсить SJ. 0 - с первой страницы"))
            if self.sj_page_start < 0: self.sj_page_start = 0
            self.sj_page_to_parse = int(input("Сколько страниц парсить. Минимум 1"))
            if self.sj_page_to_parse < 1: self.sj_page_to_parse = 1
        else:
            self.is_sj = 0

    def check_init_data(self):
        if self.is_hh:
            print(f"Будет осуществляться парсинг HH")
            print(f"    Парсинг начнётся со страницы {self.hh_page_start}")
            print(f"    Количество обрабатываемых страниц {self.hh_page_to_parse}")

        if self.is_sj:
            print(f"Будет осуществляться парсинг HH")
            print(f"    Парсинг начнётся со страницы {self.sj_page_start}")
            print(f"    Количество обрабатываемых страниц {self.sj_page_to_parse}")

    def parse_start(self):
        if self.is_hh:
            for i in range(self.hh_page_start, self.hh_page_start+self.hh_page_to_parse):
                self.get_hh_spec_page(i)

        if self.is_sj:
            for i in range(self.sj_page_start, self.sj_page_start + self.sj_page_to_parse):
                self.get_sj_spec_page(i)

    def save_result_to_db(self):
        mongo_url = 'mongodb://localhost:27017/'
        client = MongoClient(mongo_url)
        database = client.lesson2
        collection = database.lessonnnn2

        x = collection.insert_many(self.vak_array)

        print(x.inserted_ids)


    def get_spec_list(self):
        url = "https://www.superjob.ru/vakansii/"
        request = requests.get(url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(request.text, "lxml")
        body = soup.html.body
        vakansii = body.findAll("a", attrs={"href": re.compile("/vakansii/(.*?).html")})
        result = []
        for i in range(len(vakansii)):
            result.append({"vak_name": vakansii[i].text,
                           "vak_link": vakansii[i]['href']})

        self.spec_list = result

    def chooose_spec(self):
        print(f"Список доступных профессий")
        for i in range(len(self.spec_list)):
            print(f"[{i}] - {self.spec_list[i]['vak_name']}")

        self.spec_to_parse = int(input(f"Введите число соответствующее профессии:"))

    def get_result_array(self):
        return self.vak_array

    def get_hh_spec_page(self, page=False, base_url="https://ekaterinburg.hh.ru/search/vacancy?clusters=true&enable_snippets=true&no_magic=true&area=113&from=cluster_area&showClusters=true&text="):
        final_url = f"{base_url}{self.spec_list[self.spec_to_parse]['vak_name'].replace(' ', '+')}{f'&page={page-1}' if page>1 else ''}"
        #print(final_url)
        response = requests.get(final_url, headers={'User-Agent': self.USER_AGENT})
        #print(response)
        soup = BeautifulSoup(response.text, "lxml")
        body = soup.html.body
        #print(body)
        vakansii = body.findAll("div", attrs={"class": re.compile("vacancy-serp-item__row vacancy-serp-item__row_header")})
        #print(vakansii)

        for i in range (len(vakansii)):
            #print(vakansii[i])
            vak_data = vakansii[i].find("a")
            #print(vak_data)
            vak_name = vak_data.text
            #print(vak_name)
            vak_link = vak_data.get('href')
            vak_price_min = "Не указано"
            vak_price_max = "Не указано"
            vak_price = vakansii[i].find("div", attrs={"class": "vacancy-serp-item__compensation"})
            if vak_price != None:
                temp_price = vak_price.text.replace(" руб.", "")
                temp_price = temp_price.replace(u"\xa0", "")
                if "от" in temp_price:
                    temp_price = temp_price.replace("от", "")
                    vak_price_min = temp_price
                elif "до" in temp_price:
                    temp_price = temp_price.replace("до", "")
                    vak_price_max = temp_price
                else:
                    temp_price=temp_price.split("-")
                    vak_price_min=temp_price[0]
                    vak_price_max=temp_price[1]

            print(f"Вакансия: {vak_name}")
            print(f"Максимальная ЗП: {vak_price_max}")
            print(f"Минимальная ЗП: {vak_price_min}")
            print(f"Ссылка: {vak_link}")
            print(f"Источник: {vak_link.split('/')[2]}")
            print("=========================================")
            self.vak_array.append({"vac_name": vak_name,
                                   "vac_price_max": vak_price_max,
                                   "vac_price_min": vak_price_min,
                                   "vac_link": vak_link,
                                   "vac_source": vak_link.split('/')[2]})

        time.sleep(random.randint(self.sleep_min, self.sleep_max))



    def get_sj_spec_page(self, page=False, base_url="https://www.superjob.ru"):
        final_url = f"{base_url}{self.spec_list[self.spec_to_parse]['vak_link']}{f'?page={page}' if page>1 else ''}"
        response = requests.get(final_url, headers={'User-Agent': self.USER_AGENT})
        soup = BeautifulSoup(response.text, "lxml")
        body = soup.html.body
        vakansii = body.findAll("script", attrs={"type": "application/ld+json"})
        json_vak = json.loads(vakansii[1].text)

        for row in json_vak["itemListElement"]:
            response2 = requests.get(row["url"], headers={'User-Agent': self.USER_AGENT})
            soup2 = BeautifulSoup(response2.text, "lxml")
            cur_vakansija = soup2.html.body.findAll("script", attrs={"type": "application/ld+json"})
            json_cur_vakansija = json.loads(cur_vakansija[1].text)
            print(f"Вакансия: {json_cur_vakansija['title']}")

            min_price = "Не указано"
            max_price = "Не указано"
            if json_cur_vakansija.get('baseSalary', False):
                if json_cur_vakansija['baseSalary'].get('value', False):
                    if json_cur_vakansija['baseSalary']['value'].get('minValue', False):
                        min_price = json_cur_vakansija['baseSalary']['value']['minValue']
                    if json_cur_vakansija['baseSalary']['value'].get('maxValue', False):
                        max_price = json_cur_vakansija['baseSalary']['value']['maxValue']

            print(f"Максимальная ЗП: {max_price}")
            print(f"Минимальная ЗП: {min_price}")
            print(f"Ссылка: {json_cur_vakansija['url']}")
            print(f"Источник: {json_cur_vakansija['url'].split('/')[2]}")
            print("=========================================")

            self.vak_array.append({"vac_name": json_cur_vakansija['title'],
                                   "vac_price_max": max_price,
                                   "vac_price_min": min_price,
                                   "vac_link": json_cur_vakansija['url'],
                                   "vac_source": json_cur_vakansija['url'].split('/')[2]})

            time.sleep(random.randint(self.sleep_min, self.sleep_max))


if __name__ == "__main__":
    parse_jobs = findJob()
    parse_jobs.get_spec_list()
    parse_jobs.get_init_data()
    parse_jobs.parse_start()
    parse_jobs.save_result_to_db()
    print(1)

print(4)
exit(0)
