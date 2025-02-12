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
driver.get('http://127.0.0.1:5000/home')

np.random.seed(42)  # Define a aleatoriedade fix

clicks = 10000
for click in range(clicks):
    button_color = driver.find_element(
        'name', 'yescheckbox').get_attribute('value')

    if button_color == 'blue':
        if np.random.random() < 0.30:
            driver.find_element('name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            # time.sleep(0.2)
        else:
            driver.find_element('name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            # time.sleep(0.2)

    else:
        if np.random.random() < 0.40:
            driver.find_element('name', 'yescheckbox').click()
            driver.find_element('id', 'yesbtn').click()
            # time.sleep(0.2)
        else:
            driver.find_element('name', 'nocheckbox').click()
            driver.find_element('id', 'nobtn').click()
            # time.sleep(0.2)
    time.sleep(0.05)
