from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(host='localhost',
                                        database='maldoror',
                                        user='root',
                                        password='')
mycursor = connection.cursor()
PATH = "C:\Program Files (x86)\chromedriver.exe" 
driver = webdriver.Chrome(PATH)
driver.get("https://maldoror.hr/kategorija-proizvoda/merchandise/majice/")
action = webdriver.ActionChains(driver)
nebitan = driver.find_element_by_class_name("et_pb_row")
driver.maximize_window()
def jednaStranica(koliko):
    t0 = time.time()
    for i in range(koliko):
        praznaLista = []
        slike = driver.find_elements_by_class_name("et_shop_image")
        slike[i].click()
        naslov = driver.find_element_by_tag_name("h1")
        naslov = naslov.get_attribute('innerHTML')
        print(naslov)
        cijenaUKn = driver.find_element_by_class_name("price")
        cijenaUKn = cijenaUKn.get_attribute('textContent')
        print(cijenaUKn)
        
        dostupneVelicine = driver.find_elements_by_class_name("attached")
        for i in dostupneVelicine:
            dostupnaVelicina = i.get_attribute('textContent')
            praznaLista.append(dostupnaVelicina)
        if not os.path.exists(naslov):
            os.makedirs(naslov)
        brojevi = ' , '.join(praznaLista)
        val = [naslov,cijenaUKn,brojevi]
        try:
            viseSlika = driver.find_element_by_tag_name("ol")
            sveSlike = viseSlika.find_elements_by_tag_name("li")
            sveSlikeDuzina = len(sveSlike)
            for i in range(sveSlikeDuzina):
                sveSlike[i].click()
                driver.execute_script("window.scroll(0, 0);")
                action.move_by_offset(5000, 5000)
                time.sleep(1)
                path = naslov+"/"+str(i+1)+'.png'
                with open(path, 'wb') as file:
                    l = driver.find_element_by_class_name("flex-viewport")
                    time.sleep(1)
                    file.write(l.screenshot_as_png)
                val.append(path)
            sql = "INSERT INTO majce (naslov,cijenaUKN,dostupneVelicine,slika1,slika2) VALUES (%s,%s,%s,%s,%s)"
            
            print(sveSlikeDuzina)
        except:
            print("SOTA SKAF")
            path = naslov+"/"+'1.png'
            with open(path, 'wb') as file:
                l = driver.find_element_by_class_name("wp-post-image")
                file.write(l.screenshot_as_png)
            val.append(path)
            sql = "INSERT INTO majce (naslov,cijenaUKN,dostupneVelicine,slika1) VALUES (%s, %s,%s,%s)"
        mycursor.execute(sql, val)

        print(praznaLista)
        driver.back()
        time.sleep(1)
    t1 = time.time()
    print(t1-t0)
k = 0
for i in range(29):
    time.sleep(1)
    jednaStranica(36)
    nextPage = driver.find_element_by_class_name("next")
    nextPage.click()
