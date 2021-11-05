import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ChromeSetup():
    '''
    This class is just for setting up chrome driver for selenium. 
    It can save your time when you create a class that utilise selenium. 
    Just import this, put it as inherented class, and super.__init__(). 
    '''

    def __init__(
        self,
        headless: bool = True,
    ):
        # setup ChromeOptions
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-gpu')
        # loading strategy, {'normal', 'eager', 'none'}, see https://www.selenium.dev/documentation/webdriver/page_loading_strategy/
        self.chrome_options.page_load_strategy = 'normal'
        # window size, if not headless
        if not headless:
            self.chrome_options.add_argument('--start-maximized')
        if headless or sys.platform == 'linux':
            self.chrome_options.add_argument('--headless')
        if sys.platform == 'linux':
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--disable-dev-shm-usage')
        # desired capabilities (extra for network logs)
        self.caps = DesiredCapabilities.CHROME
        self.caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        # install newest chrome driver
        self.chrome_path = ChromeDriverManager().install()

