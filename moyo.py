from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from moyo_driver import *
from moyo_good import *
import colorama
from colorama import Fore, Back, Style

def unload_one_good(lc_link_on_good: str):
    print(Fore.YELLOW + 'Товар: ' + Fore.BLACK + Back.LIGHTWHITE_EX + lc_link_on_good + Fore.RESET + Back.RESET)
    lo_good = moyo_good(lc_link_on_good)
    print(Fore.YELLOW + "Артикул: " + Fore.LIGHTGREEN_EX, lo_good.article, Fore.RESET)
    print(Fore.YELLOW + "Название:" + Fore.LIGHTGREEN_EX, lo_good.name, Fore.RESET)
    print(Fore.YELLOW + "Размеры:" + Fore.LIGHTGREEN_EX, lo_good.size_list, Fore.RESET)
    print(Fore.YELLOW + "Цена:" + Fore.LIGHTGREEN_EX, lo_good.price, Fore.RESET)
    print(Fore.YELLOW + "Цены:" + Fore.LIGHTGREEN_EX, lo_good.prices, Fore.RESET)
    print(Fore.YELLOW + "Цвета:" + Fore.LIGHTGREEN_EX, lo_good.colors, Fore.RESET)
    print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, lo_good.description, Fore.RESET)
    print(Fore.YELLOW + "Картинки:" + Fore.LIGHTGREEN_EX, lo_good.pictures, Fore.RESET)

def unload_catalog_bodo(lc_first_page_of_catalog:str, lc_filename:str):
        price = Price(lc_filename+'.csv')
        pass
        lo_bodo = WD()
        ll_list_links_on_goods = lo_bodo.Get_List_Of_Links_On_Goods_From_Catalog(lc_first_page_of_catalog)
        for g in ll_list_links_on_goods:
            if is_price_have_link(lc_filename + '.csv', g):
                print(Fore.LIGHTRED_EX, 'Товар уже имеется в прайсе:', Fore.YELLOW, g, Fore.RESET)
                continue
            try: lo_good = moyo_good(lo_bodo, g)
            except:
                try:
                    lo_bodo = WD()
                    lo_good = moyo_good(lo_bodo, g)
                except:
                    lo_bodo = WD()
                    lo_good = moyo_good(lo_bodo, g)
            if len(lo_good.size) > 0:


                price.add_good('',
                               prepare_str(lo_good.article).strip() + ' ' + prepare_str(lo_good.name).strip(),
                               prepare_str(lo_good.description),
                               prepare_str(lo_good.price).replace(',', '.'),
                               '15',
                               prepare_str(g),
                               prepare_for_csv_non_list(lo_good.pictures),
                               prepare_for_csv_list(lo_good.size)
                               )
                price.write_to_csv(lc_filename + '.csv')
        lo_bodo.driver.quit()


def isnt_empty(p_param):
    #print(p_param)
    #lb_result = False
    if p_param == None:
     #   print('None')
        lb_result = False
    if type(p_param) == str:
     #   print('String')
        if len(p_param) > 0:
           lb_result = True
        else:
           lb_result = False
    if type(p_param) == int or type(p_param) == float:
      #  print('Number')
        if p_param != 0:
           lb_result = True
        else:
           lb_result = False
    #print(type(p_param), '->', p_param)
    return lb_result





########################################################################################################################
########################################################################################################################
colorama.init()
#conn = sqlite3.connect(r"g:\BODO\database\bodo.sqlite")
#cursor = conn.cursor()
########################################################################################################################
#print(get_field_from_db_by_article_and_color("14-21U", "серый (черный)", "pictures"))
#exit()
########################################################################################################################
# проверка скачивании ссылок на страницы каталога
#wd = bodoWD()
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://bodo.su/malyshi/'))

#print(wd.Get_List_Pages_Of_Catalog('https://optom-brend.ru/abakan/bodo'))

#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://optom-brend.ru/abakan/bodo'))



if sys.argv[1] == 'good':
    wd = Login()
    print(sys.argv[1])
    print(sys.argv[2])
    good = ob_good(wd, sys.argv[2])


if sys.argv[1] == 'dump':
    wd = Login()
    links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
    print('Список товаров:', links_list)
    ln_total = len(links_list)
    ln_counter = 0
    price = Price(sys.argv[3])
    price_in_stock = Price(sys.argv[3]+'in_stock.csv')
    for link in links_list:
        ln_counter = ln_counter + 1
        print('Товар: ', link, Fore.LIGHTWHITE_EX, ln_counter, '/', ln_total, Fore.RESET)
        if is_price_have_link(sys.argv[3], link) or is_price_have_link(sys.argv[3]+'in_stock.csv', link):
            print('Товар уже имеется в прайсе')
        try:
            lo_good = moyo_good(wd, link)
        except: continue
        lc_name = lo_good.name if lo_good.name.count(lo_good.article) != 0 else lo_good.article + ' ' + lo_good.name
        ll_unique = list(set(lo_good.prices))
        print('Уникальные цены: ', ll_unique)
        if len(lo_good.prices) != len(lo_good.sizes):
            print('Несоответствие количества цен и количества товаров, пропуск.')
            continue
        for lc_uprice  in ll_unique:
            j = 0
            ll_sizes = []
            ll_prices = []
            for lc_price in lo_good.prices:
                if lo_good.prices[j] == lc_uprice:
                    try:
                        ll_sizes.append(lo_good.sizes[j])
                    except:pass
                    #ll_prices.append(lo_good.prices[j])
                j = j + 1
                print('Шаг: ', j)
            if lo_good.name.count(' - в наличии') == 0:
                price.add_good('',
                                   prepare_str(lc_name),
                                   prepare_str(lo_good.description),
                                   prepare_str( str(round(float(lc_uprice.replace(',', '.').replace(' ', ''))*float(sys.argv[4]), 2))),
                                   '15',
                                   prepare_str(''),
                                   prepare_for_csv_non_list(lo_good.pictures),
                                   prepare_for_csv_list(ll_sizes)
                                   )
                price.write_to_csv(sys.argv[3])
            else:
                price_in_stock.add_good('',
                               prepare_str(lc_name),
                               prepare_str(lo_good.description),
                               prepare_str( str(round(float(lc_uprice.replace(',', '.').replace(' ', ''))*float(sys.argv[4]), 2))),
                               '15',
                               prepare_str(''),
                               prepare_for_csv_non_list(lo_good.pictures),
                               prepare_for_csv_list(ll_sizes)
                               )
                price_in_stock.write_to_csv(sys.argv[3]+'in_stock.csv')

    reverse_csv_price(sys.argv[3]+'in_stock.csv')
    reverse_csv_price(sys.argv[3])
