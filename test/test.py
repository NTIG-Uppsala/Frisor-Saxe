import unittest
import sys
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class TestClass(unittest.TestCase):
    website_image_path = Path(__file__).resolve().parents[1] / Path('root/assets/images/')
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
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        control_texts = [
            "Frisör Saxé",
            "Öppettider",
            "Mån-Fre",
            "10 - 16",
            "Lördag",
            "12 - 15",
            "Söndag",
            "Stängt",
            "Info",
            "Hej! Vi är en grupp frisörer och vi klipper folk dagligen",
            "Kontakt",
            "0630-555-555",
            "info@ntig-uppsala.github.io",
            "Hitta oss!",
            "Fjällgatan 32H",
            "981 39, Kiruna",
        ]

        for text in control_texts:
            self.assertIn(text, page_text)
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
            print(f"{social} element found")
            ActionChains(icon_element).move_to_element(icon_element).click()
            icon_href = icon_element.get_attribute("href")

            self.assertEqual(icon_href, f"https://{social}.com/ntiuppsala")
            print(f"{social} successfully clicked")



    def test_screenshot(self):
        self.driver.get(self.website_url)
    
        resolutions = [
            [2560, 1440], # 2k desktop
            [1920, 1080], # desktop
            [1440, 1080], # laptop
            [820, 1180], # iPad Air
            [390, 844], # iPhone 12 Pro
        ]

        for res in resolutions:
            x,y = res

            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(x, y)
            self.driver.save_screenshot("test/screenshots/screenshot" + str(x) + "x" + str(y) + ".png")
            print("saved screenshot with resolution", x, y)

            self.driver.set_window_size(y, x)
            self.driver.save_screenshot("test/screenshots/screenshot" + str(y) + "x" + str(x) + "landscape.png")
            print("saved screenshot with resolution", y, x)
            

    def test_for_large_images(self):
        # Assert check for images larger than 1Mb
        for image in self.website_image_path.glob('**/*.*'):
            # Get the file size property
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            # Assert if the file is greater than 500kb
            self.assertGreater(5e5, image_size)
    
    def test_for_images_on_page(self):
        self.driver.get(self.website_url)

        # get all elements with img tag
        image_elements = self.driver.find_elements(By.TAG_NAME, 'img')
        website_image_paths = []

        for image in image_elements:
            _path = ""
            if image.get_attribute('src') is not None: # if the img has a src attribute with the image
                # get src and resolve it as Pathlib Path
                _path = Path(image.get_attribute('src'))
            elif image.value_of_css_property("background-image") is not None: # if the img has a background-image css property
                # get src and resolve it as Pathlib Path
                _path = Path(image.value_of_css_property("background-image"))
            else: # assert False (Just a fail)
                self.assertTrue(False)
                continue
            
            # append paths filename to paths list
            website_image_paths.append(_path.name)

        # assert if all images are present on screen
        for image in self.website_image_path.glob('**/*.jpg'):
            print("Currently chcking if {} is in {}".format(image.name, website_image_paths))
            self.assertIn(image.name, website_image_paths)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestClass.website_url = sys.argv.pop() # Change url to passed in argument
    else:
        TestClass.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"

    unittest.main(verbosity=2) # Run unit tests
    