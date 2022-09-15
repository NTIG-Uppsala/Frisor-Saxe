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


class TestClass(unittest.TestCase):
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

        self.addCleanup(self.driver.quit) # Closes browser instance when tests are done

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
            "Långt hår",
            "600 kr",
            "Kort hår",
            "300 kr",
            "Färgning",
            "560 kr",
            "Skägg",
            "150 kr",
            "Toppning",
            "200 kr",
            "Extensions kort",
            "300 kr",
            "Extensions normal",
            "500 kr",
            "Extensions lång",
            "400 kr",
            "Barn 0-13",
            "150 kr",
            "Långt hår stamkund",
            "150 kr",
            "Kort hår stamkund",
            "500 kr",
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
            icon_element = self.driver.find_element(
                By.CLASS_NAME, f"fa-{social}")
            print(f"{social} element found")
            ActionChains(icon_element).move_to_element(icon_element).click()
            icon_href = icon_element.get_attribute("href")

            self.assertEqual(icon_href, f"https://{social}.com/ntiuppsala")
            print(f"{social} successfully clicked")

    def test_screenshot(self):
        # reference: https://www.browserstack.com/guide/ideal-screen-sizes-for-responsive-design
        resolutions = [
            [1920, 1080 , "1920x1080"],
            [2560, 1440, "2560x1440"],  # 2k desktop
            [1366, 768, "1366x768"],
            [360, 640 , "360x640"],  
            [820, 1180, "820x1180"], 
            [414, 896, "414x896"], 
            [1536, 864, "1536x864"],  
        ]

        page_sections = [
            "header",
            "openhours",
            "products",
            "contact"
        ]
        for res in resolutions:
            x, y, device_name = res

            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(width=x, height=y)
            
            for section in page_sections:
                image_path = Path(__file__).resolve().parent / Path(f'screenshots/{device_name}')
                screenshot_path = str(image_path) + f"/{section}_{device_name}.png"

                # Check if screenshots folder exists
                # example path: 'C:\\Users\\..\\Frisor-Saxe\\test\\test.py\\screenshots\\device_name'
                if not Path(image_path).exists():
                    # if not, create it
                    Path(image_path).mkdir(parents=True)

                self.driver.get(self.website_url + f"#{section}") # open the page
                time.sleep(5) # sleep for 5 seconds to let the page load
                
                try:
                    current_section_element = self.driver.find_element(By.ID, section) # find the section
                    ActionChains(current_section_element).move_to_element(current_section_element) # Move to the section
                    WebDriverWait(self.driver, 20).until(EC.visibility_of((current_section_element))) # Wait for the section to be visible
                    current_section_element.screenshot(screenshot_path) # Take screenshot of section
                    print("saved screenshot with", device_name, "at", section)
                except Exception as err:
                    # Catch any errors and print them and continue
                    print(err)
                    print("Could not save screenshot of", section, "with", device_name)
        
        # assert the correct amount of images
        expected_images = len(resolutions) * len(page_sections)
        actual_images = len(list(Path(__file__).resolve().parent.glob('screenshots/**/*.png')))
        self.assertEqual(expected_images, actual_images)

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


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestClass.website_url = sys.argv.pop()  # Change url to passed in argument
    else:
        TestClass.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"

    unittest.main(verbosity=2)  # Run unit tests
