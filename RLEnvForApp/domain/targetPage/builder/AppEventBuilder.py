from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter

class AppEventBuilder:
    _xpath:str = None
    _value:str = None
    _category:int = None

    def setValue(self, value:str):
        self._value = value

    def setXpath(self, xpath:str):
        self._xpath = XPathFormatter.format(xpath)

    def setCategory(self, category:int):
        self._category = category

    def build(self) -> AppEvent:
        return AppEvent(self._xpath, self._value, self._category)