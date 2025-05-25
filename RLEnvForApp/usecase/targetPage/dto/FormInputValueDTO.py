from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class FormInputValueDTO:
    def __init__(self, app_event_dto_list: [AppEventDTO], page_dom: str, form_xpath: str):
        self._app_event_dto_list = app_event_dto_list
        self._page_dom = page_dom
        self._form_xpath = form_xpath

    def getInputValueDTOList(self) -> [AppEventDTO]:
        return self._app_event_dto_list

    def getPageDom(self) -> str:
        return self._page_dom

    def getFormXPath(self) -> str:
        return self._form_xpath
