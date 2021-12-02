from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import requests

url = "https://md5decrypt.net/en/Api/api.php?hash="
email = "___EMAIL____"
code = "___SECRET_API_CODE____" #https://md5decrypt.net/en/Api/

id = input("Podaj ID: ")

driver = webdriver.Chrome()
driver.get('https://testy.gdynianka.pl/student/index/0/' + str(id))

time.sleep(3)
testy = driver.find_elements_by_class_name("list-group-item")
for i in range(2, len(testy)):
    print(str(i-1) + " " + testy[i].text)
odpowiedz = int(input("Podaj index testu: "))
testy[odpowiedz+1].find_element_by_tag_name("a").click()

imie = driver.find_element_by_name("imie")
imie.send_keys("anonymous")
md5 = driver.find_element_by_name("md5").get_attribute('value')
response = requests.request("GET", f"{url}{md5}&hash_type=md5&email={email}&code={code}")
haslo = driver.find_element_by_name("haslo")
haslo.send_keys(response.text)
js='document.getElementById("ilosc").value = 100;document.getElementById("tylko_zalogowani").value = 0;document.getElementById("minuty").value = 30;document.getElementById("zmien_kolejnosc_pytan").value = 0;document.getElementById("zmien_kolejnosc_odpowiedzi").value = 0;document.getElementById("tryb_nauki").value = 1;'
driver.execute_script(js);
przycisk = driver.find_element_by_xpath("/html/body/div/form/button")
przycisk.click()
time.sleep(1)
js='alert(keys)'
driver.execute_script(js)
alert = driver.switch_to.alert
pytania = alert.text
id_pytan = pytania.split(",")
alert.accept()
odpowiedzi = []
plik = open("odpowiedz.txt", "w", encoding="utf-8")
for i, pytanie in enumerate(id_pytan):
      tresc = driver.find_element_by_id(pytanie).find_element_by_class_name("panel-heading").find_element_by_tag_name("b").get_attribute('innerHTML')
      elementy = driver.find_element_by_id(f"odpowiedz{pytanie}").find_elements_by_tag_name("a")
      wynik = f"{tresc}: "
      for element in elementy:
            if 'list-group-item-success' in element.get_attribute('class').split():
                  wynik+=element.get_attribute('innerHTML')
                  wynik+=" | "
      print(wynik[:-3])
      plik.write(wynik[:-3]+'\n')
plik.close()
