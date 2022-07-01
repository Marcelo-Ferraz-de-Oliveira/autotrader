import os
from time import sleep
from headless_webdriver import *

# URL_CLEAR = os.getenv("URL_CLEAR")
URL_CLEAR_LOGIN = "https://login.clear.com.br/pit/login/"
URL_CLEAR = "https://pro.clear.com.br/#renda-variavel/swing-trade"
CPF=os.getenv("CPF")
DATA_NASCIMENTO=os.getenv("DATA_NASCIMENTO")
SENHA=os.getenv("SENHA")
ASSINATURA=os.getenv("ASSINATURA")

# print(CPF)
driver = get_headless_selenium_webdriver()
session_id = driver.session_id
driver.get(URL_CLEAR_LOGIN)
cpf_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'Username')))
cpf_field.send_keys(CPF)
contents = driver.find_elements(By.XPATH, '//h2[@class="sub_title"]')
for content in contents:
    print(content.get_attribute('innerHTML'))
data_nascimento_field = driver.find_element(By.NAME, 'DoB')
data_nascimento_field.send_keys(DATA_NASCIMENTO)
senha_field = driver.find_element(By.NAME, "Password")
senha_field.send_keys(SENHA)
acessar = driver.find_element(By.CLASS_NAME, "bt_signin")
acessar.click() 
menu = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, 'menu')))
# menu.click()
# sleep(1)
# swing_trade = driver.find_element(By.LINK_TEXT, 'Swing Trade')
# swing_trade.click()
sleep(1)
driver.get(URL_CLEAR)
# print(driver.page_source)
abev3_value = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site")))
driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
while True:
    sleep(2)
    # abev3_tile = driver.find_element(By.XPATH, "//div[@class='cont_list_equities']")
    # abev3_tile.click()
    abev3_book = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cont_detail detail-deal-book']")))
    abev3_book_prices = driver.find_elements(By.XPATH, "//div[@class='body-scr-book")
    # print(abev3_book.get_attribute('innerHTML'))
    for element in abev3_book_prices:
        print(element.get_attribute('innerHTML'))


# driver.get(URL_CLEAR)

# import cloudscraper

# scraper = cloudscraper.create_scraper(delay=5)
# req = scraper.get(URL_CLEAR)
# print(req.text)

# import undetected_chromedriver as uc

# driver = uc.Chrome()
# req = driver.get(URL_CLEAR)
# print(req.text)