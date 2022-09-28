from navigator.Navigator import Navigator
from abc import ABC, abstractmethod
import time
from csv import writer

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

BASE_URL = "https://nft.gamestop.com/collection/"
LOAD_WAIT_TIME = 10

class GSNFTCollectionNavigator(Navigator):

    link = BASE_URL
    driver = None
    pageNum = 1
    items = None

    def __init__(self, collectionName):
        self.link += collectionName
        self.driver = webdriver.Firefox()
        self.driver.get(self.link)
        self.initItems()
        self.main_handle = self.driver.current_window_handle

    # Pull each item of interest on the page into an iterable list: self.items
    def initItems(self):
        cardList = WebDriverWait(self.driver, LOAD_WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.XPATH, '//ul[contains(@class,"CardList")]') # Container with class "CardList" holds items of interest (tokens)
                )
            )
        self.items = cardList.find_elements(By.XPATH, '//a[starts-with(@href,"/token/")]') # Links for items inside cardList

    '''
    @input: label
    Attempt to retrieve hyperlinks with given aria-label attribute equal to input label
    '''
    def clickButtonAriaLabel(self, label):
        button = WebDriverWait(self.driver, LOAD_WAIT_TIME).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//a[@aria-label="{label}"]')
                )
            )
        if button.get_attribute("disabled"):
            raise Exception(f'{label} is disabled')
        else:
            button.click()

    # Go to next page and load new list of items into state
    def nextPage(self):
        self.clickButtonAriaLabel("Next page")
        self.pageNum += 1
        self.initItems()
        print(self.pageNum, self.driver.current_url)

    # Go to next page and load list of items into state
    def previousPage(self):
        self.clickButtonAriaLabel("Previous page")
        self.pageNum -= 1
        self.initItems()
        print(self.pageNum, self.driver.current_url)

    # Iterate items
    def nextItem(self):
        if not self.items:
            return None
        return self.items.pop(0)

    @abstractmethod
    def extractItem(self):
        pass

    def cleanUp(self):
        self.driver.close()




class MetaBoyNavigator(GSNFTCollectionNavigator):

    COLLECTION_NAME = "MetaBoy"
    OUTPUT_FILENAME = "metaboys.csv"
    desiredText = ""

    def __init__(self, desiredText):
        super().__init__(self.COLLECTION_NAME)
        self.desiredText = desiredText

    def writeInfo(self, ls):
        with open(self.OUTPUT_FILENAME, "a") as f:
            writer_obj = writer(f)
            writer_obj.writerow(ls)
            f.close()

    def extractItem(self, item):
        driver = self.driver

        main_handle = driver.current_window_handle
        # Open item in new tab
        item.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[-1])
        #scrape info
        try:
            section = WebDriverWait(driver, LOAD_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'MetaProperties')]")))
            name = driver.find_element(By.TAG_NAME, "h1").text
            print(f'\r{name}', end="\r")
            WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{self.desiredText}']")))
            url = driver.current_url
            print("\rFound:", name, url)
            spans = section.find_elements(By.TAG_NAME, "span")
            ls = list(map(lambda x: x.text, spans))
            ls = [name, url, self.pageNum]+ls
            self.writeInfo(ls)
        except Exception as e:
            pass
        #close tab
        driver.close()
        driver.switch_to.window(main_handle)
