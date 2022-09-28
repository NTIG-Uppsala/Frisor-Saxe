import unittest
import sys
import requests
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class TestGlobal(unittest.TestCase):
    """
        This class is used to test features that needs to be on all webpages
    """

    website_image_path = Path(__file__).resolve().parents[1] / Path('root/assets/images/')
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
            'index-fi.html',
            'personal-fi.html',
            'hitta-hit-fi.html'
        ]

    # def test_validate_code_on_page(self):
    #     validators = [
    #         "https://validator.w3.org/",
    #         "https://jigsaw.w3.org/css-validator/",
    #         ]
    #     for validator in validators:
    #         self.driver.get(validator)
    #         wait = WebDriverWait(self.driver, 10)
    #         wait.until(EC.visibility_of_element_located((By.ID, "uri")))
    #         for page in self.pages:
    #             self.driver.save_screenshot("test.png")
    #             input_element = self.driver.find_element(By.ID, "uri")
    #             self.driver.find_element(By.ID, 'uri').clear()
    #             input_element.send_keys(self.website_url + page)
    #             self.driver.save_screenshot("test_after.png")
    #             # self.driver.find_element(By.ID, "uri").send_keys(self.website_url + page)
    #             self.driver.find_elements(By.CLASS_NAME, "submit")[0].click()
    #             print("loop test pass")



    def test_find_text_on_page(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)

            print("Testing on page: {}".format(page))

            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            control_texts = [
                "Frisör Saxé",
                "Aukijat",
                "Ottaa yhteyttä",
                "0630-555-555",
                "info@ntig-uppsala.github.io",
                "Etsi täältä",
                "Fjällgatan 32H",
                "981 39, Kiruna",
                "Kartta meille"
            ]

            for text in control_texts:
                self.assertIn(text, page_text)

    def test_check_for_empty_links(self):

        for page in self.pages:
            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            links = self.driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                self.assertNotEqual(link.get_attribute("href").split("/")[-1], "#")

    def test_navigation_links(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            navigation = self.driver.find_element(By.TAG_NAME, "nav")
            links = navigation.find_elements(By.TAG_NAME, "a")

            page_text = self.driver.find_element(By.TAG_NAME, "body").text

            link_text = [
                "Koti",
                "Henkilökunta",
                "Etsi täältä"
            ]

            for text in link_text:
                self.assertIn(text, page_text)

            # check if all required links are in the navigation
            for link in self.pages:
                self.assertIn(link, [link.get_attribute("href").split('/')[-1] for link in links])

    def test_for_icons_on_page(self):
        for page in self.pages:

            self.driver.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            # List of social medias
            socials = ['facebook', 'instagram', 'twitter']

            # Loop over list
            for social in socials:
                # Check if link and icon is on page
                icon_element = self.driver.find_element(By.CLASS_NAME, f"fa-{social}")
                print(f"{social} element found")
                ActionChains(icon_element).move_to_element(icon_element).click()
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

            for image in image_elements:
                image_source = image.get_attribute('src')

                # if the img has a src attribute with a image
                if image.get_attribute('src') is not None:
                    # Assert that the image source is fetchable from the server ( < 400 )
                    self.assertLess(requests.get(image_source).status_code, 400)
                else:  # assert False (Just a fail)
                    self.assertTrue(False)
                    continue

class TestPages(unittest.TestCase):
    website_image_path = Path(__file__).resolve().parents[1] / Path('root/assets/images/')
    website_url = ""

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)

        # Closes browser instance when tests are done
        self.addCleanup(self.driver.quit)

    def check_element_content(self, group_id, expected_table_content, element):
        # loacte table element
        group_element = self.driver.find_element(By.ID, group_id)

        # get all elements
        row_elements = group_element.find_elements(By.TAG_NAME, element)

        # combine elements text to one string
        row_text = " ".join([row.text for row in row_elements]).replace("\n", " ")

        for product in expected_table_content:
            # combine list of expected row content to one string
            product_joined = " ".join(product)

            # assert content on page
            # yield product_joined in row_text
            self.assertIn(product_joined, row_text)


    """
        INDEX TESTS
    """
    # Test for open hours
    def test_check_for_open_hours(self):
        self.driver.get(self.website_url)

        self.assertIn("Aukijat", self.driver.find_element(By.TAG_NAME, "body").text)

        # List of open hours
        open_hours = [
            ["Ma-Pe", "10 - 16"],
            ["Lauantai", "12 - 15"],
            ["Sunnuntai", "Stängt"]
        ]

        self.check_element_content("openhours", open_hours, "tr")
        # self.assertTrue(all(result))
    
    # test for services on page
    def test_check_for_products(self):
        self.driver.get(self.website_url)

        
        # List of categories
        priceCategories = ["Hinta lista", "Vakio-asiakas", "Leikkaus", "Sekalaista"]

        for categories in priceCategories:
            self.assertIn(categories, self.driver.find_element(By.TAG_NAME, "body").text)

        # List of services
        products = [
            ["Pitkät hiukset", "600 kr"],
            ["Lyhyet hiukset", "500 kr"],
            ["Värjäys", "560 kr"],
            ["Parta", "150 kr"],
            ["Täyte", "200 kr"],
            ["Hiustenpidennykset lyhyet", "300 kr"],
            ["Hiustenpidennykset välillä", "400 kr"],
            ["Hiustenpidennykset pitkät", "500 kr"],
            ["Lapset 0-13", "150 kr"],
            ["Pitkähiuksinen kanta-asiakas", "300 kr"],
            ["Lyhyet hiukset kanta-asiakas", "250 kr"]
        ]

        self.check_element_content("products", products, "tr")
        # self.assertTrue(all(result))

    """
        PERSONNEL TESTS
    """
    def test_find_personnel_on_page(self):
        self.driver.get(self.website_url + "personal-fi.html")

        self.assertIn("Vi jobbar här", self.driver.find_element(By.TAG_NAME, "body").text)

        personnel_text = [
            "Fredrik Parturi",
            "Örjan Parturi",
            "Anna Hiusmuotoilija"
        ]

        self.driver.get(self.website_url + "personal-fi.html")

        page_text = self.driver.find_element(By.TAG_NAME, "body").text.replace("\n", " ")

        for text in personnel_text:
            self.assertIn(text, page_text)

    """
        FIND US TESTS
    """
    # Check for map
    def test_check_map(self):
        self.driver.get(self.website_url + "hitta-hit-fi.html")
        map_url = "google.com/maps/embed?pb=!1m18!1m12!1m3!1d1228.0965925349935!2d20.232261859374567!3d67.86606003621222!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45d0ba6368d7c09a3%3A0xe3887ef038c559b0!2sFj%C3%A4llgatan%2032%2C%20981%2039%20Kiruna!5e0!3m2!1sen!2sse!4v1663658499040!5m2!1sen!2sse"
        map_element = self.driver.find_element(By.ID, "map")

        self.assertTrue(map_element.is_displayed())
        self.assertIn(map_url, map_element.get_attribute("src"))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        # Change url to passed in argument
        TestGlobal.website_url = arg
        TestPages.website_url = arg

    else:
        # if no argument is passed in, test on live website
        TestGlobal.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"
        TestPages.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"

    unittest.main(verbosity=2)  # Run unit tests
