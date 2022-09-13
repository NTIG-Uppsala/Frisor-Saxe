import unittest
import sys
from pathlib import Path
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



    def test_screenshot(self):
        self.driver.get("https://ntig-uppsala.github.io/Frisor-Saxe/")
    
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

    def test_for_large_images(self):
        # Get path for image folder
        image_path = Path(__file__).resolve().parents[1] / Path('root/assets/images/')
        
        # Assert check for images larger than 1Mb
        for image in image_path.glob('**/*.*'):
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            self.assertGreater(5e5, image_size)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestClass.website_url = sys.argv.pop() # Change url to passed in argument
    else:
        TestClass.website_url = "https://ntig-uppsala.github.io/Frisor-Saxe/"

    unittest.main(verbosity=2) # Run unit tests
    