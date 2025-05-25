from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


class FormInputValueEntity:
    def __init__(self, inputValueListEntities: [AppEventEntity], page_dom: str, form_xpath: str):
        self._inputValueListEntities = inputValueListEntities
        self._page_dom = page_dom
        self._form_xpath = form_xpath

    def getInputValueListEntities(self) -> [AppEventEntity]:
        return self._inputValueListEntities

    def getPageDom(self) -> str:
        return self._page_dom

    def getFormXPath(self) -> str:
        return self._form_xpath
