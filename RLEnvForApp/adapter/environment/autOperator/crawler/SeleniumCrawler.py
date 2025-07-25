import io
import re
import time
from io import StringIO
from urllib.parse import urlparse

import numpy
from lxml import etree
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO

EXPLICIT_WAITING_TIME = 5000
EVENT_WAITING_TIME = 1000
PAGE_WAITING_TIME = 1000
CRAWLER_GOTO_ROOT_PAGE_TIMEOUT = 10


class SeleniumCrawler(ICrawler):
    def __init__(self, browserName: str):
        super().__init__()
        self._browserName = browserName
        self._rootPath = ""
        self._driver = None
        self._driverWithWait = None
        self._appElementDTOs: [AppElementDTO] = []
        self._formXPath = "//form"

    def goToRootPage(self):
        goToRootPageRetryCount = 1
        isGoToRootPageSuccess = False
        isTimeOut = False
        while not (isGoToRootPageSuccess or isTimeOut):
            goToRootPageRetryCount += 1
            try:
                self._driver.get(self._rootPath)
                isGoToRootPageSuccess = "http" in self.getUrl()
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except:
                isGoToRootPageSuccess = False
            isTimeOut = not goToRootPageRetryCount < CRAWLER_GOTO_ROOT_PAGE_TIMEOUT
            time.sleep(1)
        if not isGoToRootPageSuccess:
            Logger().info("SeleniumCrawler Warning: Crawler go to root page time out.")
        return isGoToRootPageSuccess

    def reset(self, rootPath: str, formXPath: str = ""):
        self.close()
        self._driver = self._getWebDriver()
        self._driverWithWait = WebDriverWait(self._driver, EXPLICIT_WAITING_TIME / 1000.)
        if rootPath != "":
            self._rootPath = rootPath
        else:
            Logger().info(
                f"SeleniumCrawler Warning: reset to '{rootPath}', go to root page '{self._rootPath}'")
        if formXPath != "":
            self._formXPath = formXPath
        else:
            self._formXPath = "//form"
        self.goToRootPage()

    def close(self):
        if self._driver is not None:
            current_driver = self._driver
            self._driver = None
            self._driverWithWait = None
            try:
                current_driver.close()
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except Exception:
                try:
                    current_driver.close()
                except KeyboardInterrupt:
                    Logger.info("KeyboardInterrupt")
                    raise
                except Exception:
                    pass
                Logger().warning("Failed to close browser. Just ignore...")

    def getElement(self, xpath: str):
        try:
            return self._driverWithWait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except KeyboardInterrupt:
            Logger.info("KeyboardInterrupt")
            raise
        except Exception:
            return None

    def executeAppEvent(self, xpath: str, value: str):
        try:
            element = self._driverWithWait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except KeyboardInterrupt:
            Logger.info("KeyboardInterrupt")
            raise
        except Exception as exception:
            Logger().error(f"SeleniumCrawler: No such element in xpath {xpath}")
            raise exception

        if value == "":
            try:
                try:
                    self._driverWithWait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                except KeyboardInterrupt:
                    Logger.info("KeyboardInterrupt")
                    raise
                except Exception as exception:
                    Logger.warning(f"SeleniumCrawler: {xpath} can't be clicked during precondition check. Just ignore this...")
                element.click()
                time.sleep(EVENT_WAITING_TIME/1000)
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except Exception as exception:
                Logger().warning(f"SeleniumCrawler Warning: xpath: {xpath} can't be clicked")
                # raise exception
        else:
            try:
                try:
                    self._driverWithWait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                except KeyboardInterrupt:
                    Logger.info("KeyboardInterrupt")
                    raise
                except Exception as exception:
                    Logger.warning(f"SeleniumCrawler: {xpath} can't be input during precondition check. Just ignore this...")
                element.clear()
                element.send_keys(value)
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except Exception as exception:
                Logger().warning(f"SeleniumCrawler Warning: xpath: {xpath} can't be input")
                # raise exception

    def getScreenShot(self):
        PNGScreenShot = self._driver.get_screenshot_as_png()
        PILScreenShot = Image.open(io.BytesIO(PNGScreenShot))
        numpyScreenShot = numpy.array(PILScreenShot)
        return numpyScreenShot

    def getAllSelectedAppElementsDTOs(self) -> [AppElementDTO]:
        html_parser = etree.parse(StringIO(self.getDOM()), etree.HTMLParser())
        self._html = etree.tostring(html_parser).decode("utf-8")
        self._appElementDTOs: [AppElementDTO] = []
        for element in html_parser.xpath(f"{self._formXPath}//input | {self._formXPath}//textarea | {self._formXPath}//button"):
            elementXpath: str = html_parser.getpath(element)
            elementHref: str = self._getHtmlTagAttribute(element, "href")
            webElement = self._driverWithWait.until(EC.presence_of_element_located((By.XPATH, elementXpath)))
            if self._isInteractable(elementXpath) and not self._shouldHrefBeIgnored(elementHref):
                self._appElementDTOs.append(AppElementDTO(tagName=element.tag,
                                                          name=self._getHtmlTagAttribute(
                                                              element=element, attribute="name"),
                                                          type=self._getHtmlTagAttribute(
                                                              element=element, attribute="type"),
                                                          placeholder=self._getHtmlTagAttribute(
                                                                element=element, attribute="placeholder"),
                                                          label=self._get_label_for_element(
                                                                html_parser=html_parser, element=element),
                                                          xpath=elementXpath,
                                                          value=webElement.get_attribute("value")))

        return self._appElementDTOs

    def changeFocus(self, xpath: str, value: str):
        return

    def getDOM(self) -> str:
        return self._driver.page_source

    def getUrl(self) -> str:
        return self._driver.current_url

    def _getWebDriver(self):
        browserName = self._browserName
        driver = None
        retry = 0
        isStartBrowser = False
        while not isStartBrowser:
            try:
                if browserName is None:
                    pass
                elif browserName == "Chrome":
                    chrome_options = webdriver.chrome.options.Options()
                    chrome_options.add_argument('--no-sandbox')  # root permission
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck,AccountConsistency,SafeBrowsingEnhancedProtection")
                    chrome_options.add_argument("--disable-default-apps")
                    # chrome_options.add_argument('--headless')  # no GUI display
                    driver = webdriver.Chrome(chrome_options=chrome_options)
                elif browserName == "Firefox":
                    firefox_options = webdriver.firefox.options.Options()
                    firefox_options.add_argument('--no-sandbox')  # root permission
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    # firefox_options.add_argument('--headless')  # no GUI display
                    driver = webdriver.Firefox(firefox_options=firefox_options)
                isStartBrowser = True
            except KeyboardInterrupt:
                Logger.info("KeyboardInterrupt")
                raise
            except:
                retry += 1
                if retry >= 10:
                    break
        driver.maximize_window()
        return driver

    def _getHtmlTagAttribute(self, element, attribute):
        try:
            attributeText = element.attrib[attribute]
        except KeyboardInterrupt:
            Logger.info("KeyboardInterrupt")
            raise
        except Exception:
            attributeText = ""
        return attributeText

    def _get_label_for_element(self, html_parser, element):
        label = ""
        try:
            label_element = html_parser.xpath(f"//label[@for='{element.attrib['id']}']")[0]
            label = label_element.text
        except KeyboardInterrupt:
            Logger.info("KeyboardInterrupt")
            raise
        except:
            label = ""
        return label

    def _isInteractable(self, xpath):
        try:
            element = self._driverWithWait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            if self._getHtmlTagAttribute(element=element, attribute="input") == "input" and self._getHtmlTagAttribute(element=element, attribute="type") == "hidden":
                return False
            return element.is_displayed() and element.is_enabled()
        except KeyboardInterrupt:
            Logger.info("KeyboardInterrupt")
            raise
        except Exception as exception:
            Logger().info(f"SeleniumCrawlerException: {exception}")
            return False

    def _shouldHrefBeIgnored(self, href: str):
        isFileDownloading = re.match(".+\\.(?:pdf|ps|zip|mp3)(?:$|\\?.+)", href)
        isMailTo = href.startswith("mailto:")
        isWebCal = href.startswith("webcal:")
        isExternal = not urlparse(href).netloc == "" and not urlparse(
            href).netloc == urlparse(self._rootPath).netloc
        return isFileDownloading or isMailTo or isExternal or isWebCal
