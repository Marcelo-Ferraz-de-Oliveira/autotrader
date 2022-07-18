import os
from time import sleep
import datetime
from webdriver import *

START_TIME = datetime.time(10, 0, 0)
END_TIME = datetime.time(16, 54, 0)

URL_CLEAR_LOGIN = "https://login.clear.com.br/pit/login/"
URL_CLEAR = "https://pro.clear.com.br/#renda-variavel/swing-trade"
CPF=os.getenv("CPF")
DATA_NASCIMENTO=os.getenv("DATA_NASCIMENTO")
SENHA=os.getenv("SENHA")
ASSINATURA=os.getenv("ASSINATURA")
SALDO_EXTERNO = float(str(os.getenv("SALDO_EXTERNO")))

VALOR_COMPRA = 13.65
VALOR_VENDA = 14.35
PRECO_HIGH_2A = 19
PRECO_LOW_2A = 12.81
DIFF_2A = PRECO_HIGH_2A - PRECO_LOW_2A

QUANTIDADE = 0

def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

def main():
    STEP = int(str(os.getenv("STEP")))
    driver = get_selenium_webdriver(headless=True)
    try:
        compra = venda = 0
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
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site")))
        driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cont_detail detail-deal-book']")))
        #mostra o livro de ofertas
        sleep(15)
        driver.find_element(By.XPATH, "//div[@class='AssetListItem ui-sortable-handle']").click()
        #Salva a assinatura eletrônica
        driver.find_element(By.XPATH, "//label[@class='checkbox bt-toggle-signature']/span[@class='check']").click()
        sleep(1)
        driver.find_element(By.XPATH, "//input[@class='relocate-signature-input']").send_keys(ASSINATURA)
        sleep(1)
        driver.find_element(By.XPATH, "//a[@class='bt-docket save-signature xsmall']").click()
        quantidade = int(str(driver.find_element(By.XPATH, "//div[@class='value detailed-net-qty']").get_attribute('innerHTML')).split(" ")[0].replace(".", ""))
        print(f"Quantidade: {quantidade}")
        preco_medio = float(str(driver.find_element(By.XPATH, "//div[@class='value detailed-net-average']").get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
        print(f"Preço médio: R${preco_medio}")
        preco_atual = float(driver.find_element(By.XPATH, "//span[@class='symbol-price']").get_attribute('innerHTML').replace(".","").replace(",","."))
        print(f"Preço atual: R$ {preco_atual}")
        driver.switch_to.default_content()
        #Clica uma vez no saldo para aparecer os elementos do saldo. Clica de novo para tirar o saldo da tela
        driver.find_element(By.XPATH, "//a[@data-wa='pit;topo-fixo;saldo-conta']").click()
        driver.find_element(By.XPATH, "//a[@data-wa='pit;topo-fixo;saldo-conta']").click()
        saldo_clear = driver.find_elements(By.XPATH, "//soma-paragraph[@class='total-amount total_val elipsed-val soma-paragraph hydrated small-text']")
        if saldo_clear:
            saldo_clear = float(str(saldo_clear[0].get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
        else:
            saldo_clear = float(str(driver.find_element(By.XPATH, "//soma-paragraph[@class='total-amount total_val elipsed-val soma-paragraph hydrated']").get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
        print(f"Saldo projetado Clear: R${saldo_clear}")
        saldo = saldo_clear + SALDO_EXTERNO
        saldo_abev3 = quantidade*preco_atual
        print(f"Saldo total dinheiro: R${saldo}")
        patrimonio = saldo + saldo_abev3
        print(f"Patrimônio total: R${patrimonio}")
        diff_percentual = 1-((preco_atual-PRECO_LOW_2A)/DIFF_2A)
        QUANTIDADE = ((patrimonio*diff_percentual)-(quantidade*preco_medio))/preco_atual
        print(f"Rebalanceamento (quantidade): {QUANTIDADE}")
        print(f"Step: {STEP}")
        driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
    except Exception as e:
        driver.close()
        print(e)
        main()

    while True:
        sleep(2)
        if not time_in_range(START_TIME, END_TIME, datetime.datetime.now().time()) or datetime.datetime.now().weekday() > 4: 
            print(f"Pregão fechado. Horário: {datetime.datetime.now()}")
            continue
        is_leilao = driver.find_elements(By.XPATH, "//div[@data-symbol='ABEV3']/div[@class='widget-list auction active']")
        if is_leilao:
            print(f"ABEV3 em Leilão")
            continue
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
        quantidade = int(str(driver.find_element(By.XPATH, "//div[@class='value detailed-net-qty']").get_attribute('innerHTML')).split(" ")[0].replace(".", ""))
        print(f"Quantidade: {quantidade}")
        preco_medio = float(str(driver.find_element(By.XPATH, "//div[@class='value detailed-net-average']").get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
        print(f"Preço médio: R${preco_medio}")
        try:
            if 0 not in (venda, compra):
                if QUANTIDADE >= STEP: 
                    abev3_venda = driver.find_element(By.XPATH, "//li[@class='action-item buy']/a")
                    abev3_venda.click()
                    abev3_qtde = driver.find_element(By.XPATH, "//input[@class='xbig input-quantity id-input-quantity ui-spinner-input']")
                    abev3_qtde.clear()
                    abev3_qtde.send_keys(STEP)
                    driver.find_element(By.XPATH, "//button[@class='btn-checkout bt-docket buy']").click()
                    print(f"Efetuada a compra de {STEP} ABEV3")
                    sleep(5)

                if QUANTIDADE <= -STEP and compra <= preco_medio: 
                    abev3_venda = driver.find_element(By.XPATH, "//li[@class='action-item sell']/a")
                    abev3_venda.click()
                    abev3_qtde = driver.find_element(By.XPATH, "//input[@class='xbig input-quantity id-input-quantity ui-spinner-input']")
                    abev3_qtde.clear()
                    abev3_qtde.send_keys(STEP)
                    driver.find_element(By.XPATH, "//button[@class='btn-checkout bt-docket sell']").click()
                    print(f"Efetuada a venda de {STEP} ABEV3")
                    sleep(5)

        except Exception as e:
            print(e)
            raise
        driver.switch_to.default_content()
        try:
            #Clica uma vez no saldo para aparecer os elementos do saldo. Clica de novo para tirar o saldo da tela
            driver.find_element(By.XPATH, "//a[@data-wa='pit;topo-fixo;saldo-conta']").click()
            driver.find_element(By.XPATH, "//a[@data-wa='pit;topo-fixo;saldo-conta']").click()
            saldo_clear = driver.find_elements(By.XPATH, "//soma-paragraph[@class='total-amount total_val elipsed-val soma-paragraph hydrated small-text']")
            if saldo_clear:
                saldo_clear = float(str(saldo_clear[0].get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
            else:
                saldo_clear = float(str(driver.find_element(By.XPATH, "//soma-paragraph[@class='total-amount total_val elipsed-val soma-paragraph hydrated']").get_attribute('innerHTML')).replace("R$ ","").replace(".", "").replace(",","."))
            saldo = saldo_clear + SALDO_EXTERNO
            saldo_abev3 = quantidade*compra
            patrimonio = saldo + saldo_abev3
            diff_percentual = 1-((compra-PRECO_LOW_2A)/DIFF_2A)
            QUANTIDADE = ((patrimonio*diff_percentual)-(quantidade*preco_medio))/compra
            STEP = int(str(os.getenv("STEP")))
            print(f"Saldo projetado Clear: R${saldo_clear}")
            print(f"Saldo total dinheiro: R${saldo}")
            print(f"Patrimônio total: R${patrimonio}")
            print(f"Rebalanceamento (quantidade): {QUANTIDADE}")
            print(f"Step: {STEP}")
        except Exception as e:
            driver.close()
            print(e)
            main()
        driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))

if __name__ == "__main__":
    main()