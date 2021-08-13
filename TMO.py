from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


username = "Canela"
options = Options()
options.add_argument("user-data-dir=C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data")
print("user-data-dir=C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data")
chromedriver = "C:\\Users\\Canela\\Documents\\ChromeDrivers\\chromedriver.exe"
print(chromedriver)
driver = webdriver.Chrome(chromedriver, options = options)
print("Accediendo a SP")
driver.get("https://lectortmo.com/items_pending/wish")
num_rows = len (driver.find_elements_by_xpath("//*[@id='app']/main/div[2]/div[1]/div[2]/div"))


#print(num_rows)


before_XPath_H="//*[@id='app']/main/div[2]/div[1]/div[2]/div["
after_XPath_H="]/a/div/div[1]/h4"
before_XPath_L="//*[@id='app']/main/div[2]/div[1]/div[2]/div["
after_XPath_L="]/a"
lista_aux=list()
lista_all=list()


for x in range(1,(num_rows+1)):
	h_text=before_XPath_H + str(x) + after_XPath_H
	head_text = driver.find_element_by_xpath(h_text).text
	lista_aux.append(head_text)
	h_text=before_XPath_L + str(x) + after_XPath_L
	link = driver.find_element_by_xpath(h_text).get_attribute('href')
	lista_aux.append(link)
	lista_all.append(lista_aux)
	lista_aux=list()

print(lista_all)
