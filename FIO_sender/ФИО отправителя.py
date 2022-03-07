import telebot
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from time import sleep
import pyperclip
import numpy
import datetime
from datetime import timedelta, datetime
import sys
import os
import re
import shutil
import httplib2
import apiclient.discovery
import gspread  # импортируем gspread
from oauth2client.service_account import ServiceAccountCredentials  # ипортируем ServiceAccountCredentials
from zeep import CachingClient, Settings, helpers

def FIO():


    # Блок запуска гугл таблицы
    link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
    my_creds = ServiceAccountCredentials.from_json_keyfile_name('krestoprav-8e5f49dc5ebe.json',
                                                                link)  # формируем данные для входа из нашего json файла
    client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами

    URL ="https://docs.google.com/spreadsheets/d/1pfzsB7fltwHyxdLyKnsK6YDNA2ffPU0LWq4SyI3Zgx8/edit#gid=715714864"
    sheet = client.open_by_url(URL).worksheet('Ответы на форму (1)')  # открываем нужную нам таблицу и лист
    # Glider

    #  Блока запуска браузера

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')

    browser = webdriver.Chrome(r'C:\Users\User\Desktop\Python\chromedriver.exe', options=options)
    browser.maximize_window()
    wait = WebDriverWait(browser, 30)

    # Первая строка в таблицу, с которой начинается обход (чтение из файла)
    file = open('1.txt', 'r', encoding='utf-8')
    n=int(file.readline())
    file.close()

    # Цикл обхода строк вкладки, пока первый столбец не пустой
    while sheet.cell(n, 1).value != None:
        # Цикл обхода ошибок при определении первого столбца и отправителя
        while True:
            try:
                a=sheet.cell(n, 18).value
                b=sheet.cell(n, 4).value
            except Exception:
                print("Ошибка при определении первого столбца и наличия ФИО")
                time.sleep(30)
                continue
            break

        # Если первый столбец с датой и столбец с треком не пустые то заполняем отправителя
        if a == None and b != None:
            print(rf"{n} заполняем")
            # Цикл обхода ошибок при получении номера трека
            while True:
                try:
                    track = sheet.cell(n, 4).value  # Получаем трек
                except Exception:
                    print("Ошибка при получении трека из таблицы")
                    time.sleep(15)
                    continue
                break
            browser.get(rf"https://www.pochta.ru/tracking#{str(track)}")  # Вводим трек в почту России
            browser.refresh()

            # Получаем ФИО отправителя
            # Цикл обхода ошибки при получении ФИО из почты России. Не более 3 раз.

            for i in range(3):
                try:
                    FIO = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-tracking"]/div/div[2]/div/div[2]/div[2]/div/div[3]/div[2]'))).text
                except Exception:
                    print("Ошибка почты России")
                    # В случае ошибки перезапускаем браузер и снова открываем страницу с треком
                    browser.quit()
                    browser = webdriver.Chrome(r'C:\Users\User\Desktop\Python\chromedriver.exe', options=options)
                    browser.maximize_window()
                    wait = WebDriverWait(browser, 30)
                    browser.get(rf"https://www.pochta.ru/tracking#{str(track)}")  # Вводим трек в почту России
                    browser.refresh()
                    FIO="Ошибка"
                    continue
                break

            # Если по итогу обхода цикла ФИО не получилось вытащить, то идем в следующую строку
            if FIO=="Ошибка":
                print("Ошибка почты России, пропускаем")
                n+=1
                file = open('1.txt', 'w', encoding='utf-8')
                file.write(str(n))
                file.close()
                continue

            # Цикл обхода ошибки при форматировании
            for i in range(2):
                print(rf"{FIO} на итерации № {i}")
                try:
                    FIO = str(FIO).split(": ")[1]  # Форматируем имя отправителя
                except Exception:
                    if i==0:
                        FIO = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="page-tracking"]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[2]'))).text
                        continue
                    if i==1:
                        print("Ошибка при форматрировании")
                        FIO = "Ошибка"
                break


            # Если по итогу обхода цикла ФИО не получилось отформатировать, то идем в следующую строку
            if FIO=="Ошибка":
                n+=1
                file = open('1.txt', 'w', encoding='utf-8')
                file.write(str(n))
                file.close()
                continue

            # цикл обхода ошибки при вставке ФИО в таблицу
            while True:
                try:
                    sheet.update_cell(n, 18, FIO)
                except Exception:
                    print("Ошибка при вставке трека в таблицу")
                    time.sleep(15)
                    continue
                break
            browser.refresh()
        else:
            print(rf"{n} пропускаем")
            time.sleep(2)
        n+=1
        file = open('1.txt', 'w', encoding='utf-8')
        file.write(str(n))
        file.close()


    browser.quit()  # Закрываем браузер по окончанию цикла
    print("Список закончился")

    # Прописываем начальную строку в файл для начала следующего цикла
    file = open('1.txt', 'w', encoding='utf-8')
    file.write(str(2))
    file.close()

while True:

    try:
        FIO()
    except Exception:
        continue
    break

