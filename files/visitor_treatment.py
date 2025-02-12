from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import numpy as np
import time

# Defina o caminho para o ChromeDriver
path_webdriver = "D:/Comunidade DS/teste_a_b/pa_bayseian/chromedriver.exe"

# Configure o serviço do ChromeDriver
service = Service(path_webdriver)

# Inicialize o driver com o serviço configurado
driver = webdriver.Chrome(service=service)

# Acesse a página desejada
driver.get('http://127.0.0.1:5001/home')

np.random.seed(42)  # Define a aleatoriedade fixa

clicks = 10000
for click in range(clicks):
    if np.random.random() < 0.4:
        # driver.find_element('name', 'yescheckbox').click()
        driver.find_element('id', 'yesbtn').click()
        time.sleep(0.5)
    else:
        # driver.find_element('name', 'nocheckbox').click()
        driver.find_element('id', 'nobtn').click()
        time.sleep(0.5)
