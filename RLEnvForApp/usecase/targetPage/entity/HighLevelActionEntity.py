from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


class HighLevelActionEntity:
    def __init__(self, appEventEntities: [AppEventEntity], page_dom: str, form_xpath: str):
        self._appEventEntities = appEventEntities
        self._page_dom = page_dom
        self._form_xpath = form_xpath

    def getAppEventEntities(self) -> [AppEventEntity]:
        return self._appEventEntities

    def getPageDom(self) -> str:
        return self._page_dom

    def getFormXPath(self) -> str:
        return self._form_xpath
