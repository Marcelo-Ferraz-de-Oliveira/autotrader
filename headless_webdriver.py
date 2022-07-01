from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def get_headless_selenium_webdriver():
  options = webdriver.ChromeOptions()
  # options.add_argument('--headless')
  # options.add_argument('--no-sandbox')
  # options.add_argument('--disable-dev-shm-usage')
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_experimental_option('useAutomationExtension', False)
  prefs = {"download.default_directory" : "."}
  options.add_experimental_option('prefs',prefs)
  return webdriver.Chrome('chromedriver',options=options)