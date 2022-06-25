from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

class WD:
    def init(self):
        config = configparser.ConfigParser()
        config.read("Login.ini")
        print(config["Login"]["Login"], config["Login"]["Password"])
        lc_link = r'https://moyo.moda/zhen/catalog/jenskoe-belye-aksessuary/eroticheskoye-belyo-jenskoe-belye/'
        print(Fore.RED + 'Chrome Web Driver '+Fore.YELLOW +lc_link+Fore.RESET)
        
        if True:
            chrome_options = webdriver.ChromeOptions()
            chrome_prefs = {}
            chrome_options.experimental_options["prefs"] = chrome_prefs
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()


        self.Get_HTML(lc_link)
        time.sleep(1)
        link = self.driver.find_element(by=By.PARTIAL_LINK_TEXT, value=r'Вход/Регистрация')
        link.click()
        time.sleep(1)
        self.driver.find_element(by=By.NAME, value = "Login").send_keys(config["Login"]["Login"])
        self.driver.find_element(by=By.NAME, value = "Password").send_keys(config["Login"]["Password"])
        self.driver.find_element(by=By.XPATH, value = "//*[contains(@class,'afarr')]").click()
        self.Get_HTML(lc_link)
    def __init__(self):
        self.init()

    def __del__(self):
        try:
            #self.driver.quit()
            pass
        except: pass

    def Get_HTML(self, curl):
        self.driver.get(curl)
        return self.driver.page_source

    def Get_List_Of_Links_On_Goods_From_Catalog(self, curl):
        print(Fore.RED + 'Список товаров каталога: ' + Fore.YELLOW + curl + Fore.RESET)
        lst = []
        ls_links_pages_of_catalog = self.Get_List_Pages_Of_Catalog(curl)
        print('==========================', ls_links_pages_of_catalog)
        for link_on_page_of_catalog in ls_links_pages_of_catalog:
            print(Fore.YELLOW + 'Страницы каталога и товары на них: ' + Fore.LIGHTYELLOW_EX + link_on_page_of_catalog + Fore.RESET)
            print('Переходим: ', link_on_page_of_catalog)
            self.Get_HTML(link_on_page_of_catalog)
            elements = self.driver.find_elements(by=By.CLASS_NAME, value='product-item__content')
            for element in elements:
                lc_link = sx(element.get_attribute('innerHTML'), '<a href="','"')
                if lc_link not in lst:
                    lst.append(lc_link)
        return lst

    def Get_Link_On_Next_Catalog_Page(self):
        lc_link = ''
        try:
                lc_link = self.driver.find_element_by_xpath("//*[contains(@class,'tx_next fa fa-chevron-right')]").get_attribute('href')
        except: pass
        return lc_link

    def Get_List_Pages_Of_Catalog(self, c_link_on_first_catalog):
        self.driver.get(c_link_on_first_catalog)
        print(2)
        lo_navigation = self.driver.find_element(by=By.XPATH, value = "//*[contains(@class,'page_navi__prev_next_block')]")
        print(lo_navigation.get_attribute('InnerHTML'))


        return []

    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.driver.page_source)
        file.close()


def Login():
    try:
        wd = WD()
        print(1)
    except:
        try:
            wd = WD()
            print(2)
        except:
            try:
                wd = WD()
                print(3)
            except:
                try:
                    wd = WD()
                    print(4)
                except:
                    pass
    return wd


colorama.init()

wd = WD()
print(wd)


wd.Get_HTML(r"""http://moyo.moda/zhen/catalog/jenskoe-belye-aksessuary""")
print('---')

#    if wd.driver.page_source.count('user773')>0:
#        print('Авторизация прошла успешно')
#        return wd
#    else:
#        print('Авторизация не прошла')
#        try:
#            pass
#            wd.driver.quit()
#        except:
#            print('Рекурсивный перезапуск')
#            return LoginOB()