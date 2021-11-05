from SeleniumWebDriverSetup import ChromeSetup
from seleniumwire import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import json


class NetworkCapture(ChromeSetup):
    def __init__(self, headless: bool = False):
        super().__init__(headless=headless)
        self.seleniumwire_options = {"enable_har": True}

    def start(self):
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_path,
            options=self.chrome_options,
            seleniumwire_options=self.seleniumwire_options,
            desired_capabilities=self.caps
        )

    def goto(self, url):
        self.driver.get(url)

    def wait(self, sec=5):
        sleep(sec)

    def stop(self):
        self.driver.close()

    def get_obj_by_xapth(self, xpath) -> WebElement:
        return self.driver.find_element_by_xpath(xpath)

    def pass_text(self, web_element, text):
        return web_element.send_keys(text)

    def click_it(self, web_element):
        return web_element.click()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def log(self, what_type) -> dict:
        return self.driver.get_log(what_type)

    def get_har(self):
        return self.driver.har


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


if __name__ == "__main__":
    url = "https://www.scrapethissite.com/"
