# OBS!!! Justera inte variabelnamn då det är en del av modulerna, och kan sluta fungera om ändrade

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)

def test_find_text_on_page(driver): # Kollar att viktigt innehåll finns på hemsidan
    driver.get("https://ntig-uppsala.github.io/Frisor-Saxe/")
    pageText = driver.find_element(By.TAG_NAME, "body").text
    controlTexts = [
        "Frisör Saxé",
        "Öppettider",
        "Mån-Fre: 10-16",
        "Lördag: 12-15", 
        "Söndag: Stängt!",
        "Adress",
        "Fjällgatan 32H",
        "981 39, Kiruna",
        "Telefonnummer",
        "0630-555-555",
        "E-post",
        "info@ntig-uppsala.github.io",
    ]

    for text in controlTexts:
        assert text in pageText

def test_click_links_on_page(driver): # Klickar på länkarna för att så om dom öppnar en hemsida
    driver.find_element(By.CSS_SELECTOR, ".fa-facebook").click()
    driver.find_element(By.CSS_SELECTOR, ".fa-instagram").click()
    driver.find_element(By.CSS_SELECTOR, ".fa-twitter").click()

test_find_text_on_page(driver)
test_click_links_on_page(driver)
    
driver.quit()
