from seleniumwire import webdriver
from bs4 import BeautifulSoup
from time import sleep
from SeleniumWebDriverSetup import ChromeSetup
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque


class Extractor(ChromeSetup):
    '''
    WIP, 
    an experimental use on how much infomation can be gethered from the URL, 
    with the aid of selenium and bs4
    '''

    def __init__(self, url: str, depth: int = 1, headless: bool = False, *args, **kwargs):
        super().__init__(headless=headless)
        self.seleniumwire_options = {"enable_har": True}

    def start(self):
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_path,
            options=self.chrome_options,
            seleniumwire_options=self.seleniumwire_options,
            desired_capabilities=self.caps
        )

    def stop(self):
        self.driver.close()

    def get_obj_by_xapth(self, xpath) -> WebElement:
        return self.driver.find_element_by_xpath(xpath)

    def pass_text(self, web_element, text):
        return web_element.send_keys(text)

    def click_it(self, web_element):
        return web_element.click()

    def log(self) -> dict:
        details = {}
        return details

    def goto(self, url: str):
        self.driver.get(url)
        self.title = self.driver.title
        self.DOM_data = self.driver.page_source
        self.har = self.driver.har

    def _gather(self):
        soup = BeautifulSoup(self.DOM_data, "lxml")
        for name in dir(self.driver):
            print(f"{name}: {getattr(self.driver, name)}\n")

