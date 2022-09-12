import unittest
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class TestClass(unittest.TestCase):
    website_url = ""

    # Setup selenium options and drivers
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)


    # Checks for important info on webpage
    def test_find_text_on_page(self):
        self.driver.get(self.website_url)
        pageText = self.driver.find_element(By.TAG_NAME, "body").text
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
            "info@ntig-uppsala.github.io"
        ]

        for text in controlTexts:
            self.assertIn(text, pageText)
            # assert text in pageText
        print("All text content found!")

    def test_click_links_on_page(self):
        self.driver.get(self.website_url)

        # List of social medias
        socials = ['facebook', 'instagram', 'twitter']

        # Loop over list
        for social in socials:
            # Check if link and icon is on page
            icon_element =  self.driver.find_element(By.CLASS_NAME, f"fa-{social}")
            icon_element.click()
            icon_href = icon_element.get_attribute("href")

            self.assertEqual(icon_href, f"https://{social}.com/ntiuppsala")
            print(f"{social} passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestClass.website_url = sys.argv.pop() # Change url to passed in argument
    else:
        TestClass.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"

    unittest.main(verbosity=2) # Run unit tests
    