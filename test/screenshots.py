import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox


service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)

resolutions = [
    [2560, 1440], # 2k desktop
    [1920, 1080], # desktop
    [1440, 1080], # laptop
    [820, 1180], # iPad Air
    [390, 844], # iPhone 12 Pro
    ]

def test_screenshot(driver, res):
    driver.get("https://ntig-uppsala.github.io/Frisor-Saxe/")
    x,y = res
    driver.set_window_position(0, 0)
    driver.set_window_size(x, y)
    driver.save_screenshot("test/screenshots/screenshot" + str(x) + "x" + str(y) + ".png")
    print("saved screenshot with resolution", x, y)

for res in resolutions:
    test_screenshot(driver, res)
driver.quit()