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

VALOR_LIMITE = 13.80
QUANTIDADE = 1000


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
sleep(1)
driver.get(URL_CLEAR)
abev3_value = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site")))

driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
compra = venda = 0
abev3_book = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cont_detail detail-deal-book']")))
try:
    #mostra o livro de ofertas
    driver.find_element(By.XPATH, "//div[@class='AssetListItem ui-sortable-handle']").click()
except Exception as e:
    print(e)

try:
    #Salva a assinatura eletrônica
    driver.find_element(By.XPATH, "//label[@class='checkbox bt-toggle-signature']/span[@class='check']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//input[@class='relocate-signature-input']").send_keys(ASSINATURA)
    sleep(1)
    driver.find_element(By.XPATH, "//a[@class='bt-docket save-signature xsmall']").click()
except Exception as e:
    print(e)

while True:
    sleep(2)
    try:
        #Fica clicando em venda e colocando o valor
        abev3_venda = driver.find_element(By.XPATH, "//li[@class='action-item sell']/a")
        abev3_venda.click()
        abev3_qtde = driver.find_element(By.XPATH, "//input[@class='xbig input-quantity id-input-quantity ui-spinner-input']")
        abev3_qtde.clear()
        abev3_qtde.send_keys(QUANTIDADE)
    except Exception as e:
        print(e)
    abev3_book_prices = driver.find_elements(By.XPATH, "//tbody[@class='itens']/tr/td[@class='buy-amount buy']/a")
    for key, element in enumerate(abev3_book_prices):
        if key == 0:
            compra = float(str(element.get_attribute('innerHTML')).replace('<var>', '').replace('</var>', '').replace('Aber', '0')) 
            print(f"ABEV3 compra: {compra}")
    abev3_book_prices = driver.find_elements(By.XPATH, "//tbody[@class='itens']/tr/td[@class='sell-amount sell']/a")
    for key, element in enumerate(abev3_book_prices):
        if key == 0: 
            venda = float(str(element.get_attribute('innerHTML')).replace('<var>', '').replace('</var>', '').replace('Aber', '0')) 
            print(f"ABEV3 venda: {venda}")