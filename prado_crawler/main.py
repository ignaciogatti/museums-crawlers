from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import subprocess

BASE_PATH = '/home/ignacio/Devel/crawler/prado_crawler/image_sequence'

def get_initial_urls():

    browser = webdriver.Chrome()
    browser.get('https://www.museodelprado.es/en/mi-prado/recorridos-recomendados')

    PAUSE_TIME = 3
    time.sleep(PAUSE_TIME)
    
    #Cookie button
    cookie_button = browser.find_element_by_css_selector('div.cookies-msg div.wrap a.botones-centrados.bt-aceptar.bc-estandar.hv-estandar')
    cookie_button.click()
    time.sleep(PAUSE_TIME)

    #Find "ver mas" button
    next_button = browser.find_element_by_css_selector('div.ver-mas-general a')
    more_data = next_button.is_displayed()

    #load all images
    while more_data:
        #time.sleep(PAUSE_TIME)
        actions = ActionChains(browser)
        actions.move_to_element(next_button).perform()
        next_button.click()
        time.sleep(PAUSE_TIME)
        #try to check if there is more data to load
        try:
            next_button = browser.find_element_by_css_selector('div.ver-mas-general a')
            more_data = next_button.is_displayed()
        except:
            more_data = False

    urls_elements = browser.find_elements_by_css_selector('div.rec figure div a')
    urls = []
    for element in urls_elements:
        urls.append(element.get_attribute("href"))
    
    return urls




#get urls
urls = get_initial_urls()

process_path = os.path.join(os.getcwd(), 'crawler_process.py')
print(process_path)

index = 0
for url in urls:

    subprocess.run("python " + process_path + " " + str(index) + " " + url, shell=True  )
    index += 1