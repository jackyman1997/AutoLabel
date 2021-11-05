from .setup.SeleniumWebDriverSetup import ChromeSetup  # my own setup class
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import urllib
from PIL import Image
from bs4 import BeautifulSoup
from time import sleep
import datetime
import typing
import boto3
import validators
import json
import os


s3_client = boto3.client('s3')
s3_bucket = "webpagescreenshots"

'''
STUCK AT s3 credendials or IAM role shits 
for uploading stuff to s3, u need 4 things: 
    1. aws key
    2. aws secret key
    3. region (eu-west-2)
    4. format (json)
aws key and aws secret key are generated in pairs: 
    - simply go to aws, IAM, user, choose one, security_credentials, Access keys
    - create or choose an existing key (assuming u know the secret key)
    - then install aws cli, `aws configure` to set it up
u may also wna create a new user, a new IAM role
to reset aws keys:
    - simply delete ~/.aws/config & credentials, 
    or to change them manually (if u could)
    - `aws configure` again
to see aws keys: 
    - `aws configure list`
'''


class Stalker(ChromeSetup):
    '''
    WIP, 
    an experimental use on getting screenshot from the URL, 
    with the aid of selenium and bs4
    '''

    def __init__(
        self,
        url: typing.Union[str, list],
        headless: bool = False,
        saves3: bool = False,
        *args,
        **kwargs
    ):
        # check input ok
        if isinstance(url, str):  # if str, either path or url
            if validators.url(url):
                urls = None
            else:
                try:
                    with open(url, "r") as f:
                        url = None
                        urls = json.load(f)
                        N = len(urls)
                except:
                    raise NotImplementedError("only url or json path for now")
        else:
            raise NotImplementedError("only url or json path for now")
        # webdriver setup
        super().__init__(headless=headless)
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_path, options=self.chrome_options)
        # store in list of dict
        output = []
        # loop or no
        if urls is None:
            self._get(url)
            self._screenshot(saves3=saves3)
            self.this_data["id"] = 0
            output.append(self.this_data)
            self.driver.close()
        elif url is None:
            for i, url in enumerate(urls):
                self._get(url)
                self._screenshot(saves3=saves3)
                print(f"{i+1}/{N} done", end="\r")
                self.this_data["id"] = i
                output.append(self.this_data)
            self.driver.close()
        else:
            raise NotImplementedError("You gave me nothing and ask me work???")
        # saves output
        output_name = datetime.datetime.now().strftime("%m%d%Y%H%M%S") + ".json"
        data = json.dumps(output, indent=1)
        if saves3:
            s3_client.put_object(Bucket=s3_bucket, Body=data, Key=output_name)
        else:
            with open(output_name, 'w') as f:
                f.write(data)

    def _get(self, url: str):
        self.driver.get(url)
        sleep(1)
        self.url_parsed = urllib.parse.urlsplit(url)
        # print(self.driver.current_url, url)
        self.this_data = {}
        self.this_data["url"] = url
        self.this_data["pagesource"] = self.driver.page_source

    def _screenshot(
            self,
            web_body: WebElement = None,
            whole: bool = True,
            saves3: bool = True
    ):
        '''
        https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver/57338909#57338909
        '''
        if not whole and web_body is None:
            self.driver.close()
            raise NotImplementedError(
                """
                Bro give me a webelement, 
                you can't give me no webelement (web_body=None) 
                and don't whole whole web page screenshot (whole=False) 
                at the same time.
                """)
        # if taking whole webpage, or no specified webelement
        elif whole and web_body is None:
            # check if in headless mode
            if self.chrome_options.headless is False:
                self.driver.close()
                raise NotImplementedError(
                    "Current screenshot method only works with headless mode")

            def setSize(X):
                # function required to extend the webpage window size
                return self.driver.execute_script(
                    'return document.body.parentNode.scroll'+X)
            # set window size
            self.driver.set_window_size(
                setSize("Width"),
                setSize("Height"))
            # select html body tag as the whole page
            web_body = self.driver.find_element_by_tag_name('body')
        # save image, either locally
        title = self.driver.title
        net_loc = self.url_parsed.netloc.replace('www.', '')
        now = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        img_name = f"{title}@{net_loc}@{now}.png"
        self.this_data["title"] = title
        if saves3:
            # or return as a binary data or base64 encoded
            # see here https://selenium-python.readthedocs.io/api.html?highlight=Screenshot%20#selenium.webdriver.remote.webelement.WebElement.screenshot_as_base64
            img = web_body.screenshot_as_png
            s3_client.put_object(Bucket=s3_bucket, Body=img, Key=img_name)
            self.this_data["imgPath"] = f"s3://{s3_bucket}/{img_name}"
        else:
            web_body.screenshot(filename=img_name)
            self.this_data["imgpath"] = f"{os.getcwd()}/{img_name}"
