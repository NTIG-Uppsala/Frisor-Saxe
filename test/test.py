from re import S
import unittest
import sys
import time
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestGlobal(unittest.TestCase):
    """
        This class is used to test features that need to be on all webpages
    """

    website_image_path = Path(__file__).resolve(
    ).parents[1] / Path('root/assets/images/')
    website_url = ""

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

        # Closes browser instance when tests are done
        self.addCleanup(self.driver.quit)

        self.pages = [
            'index.html',
            # 'personal.html',
            'hitta-hit.html'
        ]

    def test_check_for_empty_links(self):

        for page in self.pages:
            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            links = self.driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                self.assertNotEqual(link.get_attribute(
                    "href").split("/")[-1], "#")

    def test_navigation_links(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            navigation = self.driver.find_element(By.TAG_NAME, "nav")
            links = navigation.find_elements(By.TAG_NAME, "a")
            required_links = [
                "index.html",
                "hitta-hit.html"
            ]

            # check if all required links are in the navigation
            for link in required_links:
                self.assertIn(link, [link.get_attribute(
                    "href").split('/')[-1] for link in links])

    def test_for_icons_on_page(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            # List of social medias
            socials = ['facebook', 'instagram', 'twitter']

            # Loop over list
            for social in socials:
                # Check if link and icon is on page
                icon_element = self.driver.find_element(
                    By.CLASS_NAME, f"fa-{social}")
                print(f"{social} element found")
                ActionChains(icon_element).move_to_element(
                    icon_element).click()
                icon_href = icon_element.get_attribute("href")

                self.assertEqual(icon_href, f"https://{social}.com/ntiuppsala")
                print(f"{social} successfully clicked")

    def test_for_large_images(self):
        # Assert check for images larger than 1Mb
        for image in self.website_image_path.glob('**/*.*'):
            # Get the file size property
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            # Assert if the file is greater than 500kb
            self.assertGreater(500_000, image_size)

    def test_for_images_on_page(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            # get all elements with img tag
            image_elements = self.driver.find_elements(By.TAG_NAME, 'img')
            website_image_paths = []

            for image in image_elements:
                _path = ""
                # if the img has a src attribute with the image
                if image.get_attribute('src') is not None:
                    # get src and resolve it as Pathlib Path
                    _path = Path(image.get_attribute('src'))
                else:  # assert False (Just a fail)
                    self.assertTrue(False)
                    continue

                # append paths filename to paths list
                website_image_paths.append(_path.name)

            # assert if all images are present on screen
            for image in self.website_image_path.glob('**/*.jpg'):
                print("Currently chcking if {} is in {}".format(
                    image.name, website_image_paths))
                self.assertIn(image.name, website_image_paths)


class TestPersonnel(unittest.TestCase):
    website_image_path = Path(__file__).resolve(
    ).parents[1] / Path('root/assets/images/')
    website_url = ""

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

        # Closes browser instance when tests are done
        self.addCleanup(self.driver.quit)

    def test_find_text_on_page(self):
        self.driver.get(self.website_url)
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        control_texts = [
            "Frisör Saxé",
            "Öppettider",
            "Kontakt",
            "0630-555-555",
            "info@ntig-uppsala.github.io",
            "Hitta oss",
            "Fjällgatan 32H",
            "981 39, Kiruna",
            "Fredrik",
            "barberare",
            "Öjran",
            "barberare",
            "Anna",
            "hair stylist",
        ]

        for text in control_texts:
            self.assertIn(text, page_text)

    # Check content
    # Check for social links


class TestFindUs(unittest.TestCase):
    website_image_path = Path(__file__).resolve(
    ).parents[1] / Path('root/assets/images/')
    website_url = ""

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

        # Closes browser instance when tests are done
        self.addCleanup(self.driver.quit)

    # Check for map
    def test_check_map(self):
        self.driver.get(self.website_url)
        map_url = "google.com/maps/embed?pb=!1m18!1m12!1m3!1d1228.0965925349935!2d20.232261859374567!3d67.86606003621222!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45d0ba6368d7c09a3%3A0xe3887ef038c559b0!2sFj%C3%A4llgatan%2032%2C%20981%2039%20Kiruna!5e0!3m2!1sen!2sse!4v1663658499040!5m2!1sen!2sse"
        map_element = self.driver.find_element(By.ID, "map")

        self.assertTrue(map_element.is_displayed())
        self.assertIn(map_url, map_element.get_attribute("src"))

    # Check content
    def test_find_text_on_page(self):
        self.driver.get(self.website_url)
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        control_texts = [
            "Frisör Saxé",
            "Öppettider",
            "Kontakt",
            "0630-555-555",
            "info@ntig-uppsala.github.io",
            "Hitta oss",
            "Fjällgatan 32H",
            "981 39, Kiruna"
        ]

        for text in control_texts:
            self.assertIn(text, page_text)
            # assert text in pageText

    # Check for social links


class TestIndex(unittest.TestCase):
    website_image_path = Path(__file__).resolve(
    ).parents[1] / Path('root/assets/images/')
    website_url = ""

    # Setup selenium options and drivers
    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

        # Closes browser instance when tests are done
        self.addCleanup(self.driver.quit)

    # Checks for important info on webpage
    def test_find_text_on_page(self):
        self.driver.get(self.website_url)
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        control_texts = [
            "Frisör Saxé",
            "Öppettider",
            "Produkter",
            "Kontakt",
            "0630-555-555",
            "info@ntig-uppsala.github.io",
            "Hitta oss",
            "Fjällgatan 32H",
            "981 39, Kiruna"
        ]

        for text in control_texts:
            self.assertIn(text, page_text)
            # assert text in pageText

    def check_table_content(self, table_id, expected_table_content):
        # loacte table element
        table_element = self.driver.find_element(By.ID, table_id)

        # get all tr elements
        table_row_elements = table_element.find_elements(By.TAG_NAME, "tr")

        # combine tr elements text to one string
        table_row_text = " ".join(
            [table_row.text for table_row in table_row_elements])

        for product in expected_table_content:
            # combine list of expected row content to one string
            product_joined = " ".join(product)

            # assert content on page
            self.assertIn(product_joined, table_row_text)

    # Test for open hours
    def test_check_for_open_hours(self):
        self.driver.get(self.website_url)

        # List of open hours
        open_hours = [
            ["Mån-Fre", "10 - 16"],
            ["Lördag", "12 - 15"],
            ["Söndag", "Stängt"]
        ]

        self.check_table_content("openhours", open_hours)
    # test for products on page

    def test_check_for_products(self):
        self.driver.get(self.website_url)

        # List of products
        products = [
            ["Långt hår", "600 kr"],
            ["Kort hår", "500 kr"],
            ["Färgning", "560 kr"],
            ["Skägg", "150 kr"],
            ["Toppning", "200 kr"],
            ["Extensions kort", "300 kr"],
            ["Extensions normal", "400 kr"],
            ["Extensions lång", "500 kr"],
            ["Klippning barn 0-13", "150 kr"],
            ["Långt hår stamkund", "300 kr"],
            ["Kort hår stamkund", "250 kr"]
        ]

        self.check_table_content("products", products)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        # Change url to passed in argument
        TestGlobal.website_url = arg
        TestIndex.website_url = arg + "index.html"
        TestPersonnel.website_url = arg + "personal.html"
        TestFindUs.website_url = arg + "hitta-hit.html"

    else:
        # if no argument is passed in, test on live website
        TestGlobal.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"
        TestIndex.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/index.html"
        TestPersonnel.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/personal.html"
        TestFindUs.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/hitta-hit.html"

    unittest.main(verbosity=2)  # Run unit tests
