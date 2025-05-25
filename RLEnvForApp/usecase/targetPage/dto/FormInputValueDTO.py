from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class FormInputValueDTO:
    def __init__(self, input_value_dto_list: [AppEventDTO], page_dom: str, form_xpath: str):
        self._input_value_dto_list = input_value_dto_list
        self._page_dom = page_dom
        self._form_xpath = form_xpath

    def getInputValueDTOList(self) -> [AppEventDTO]:
        return self._input_value_dto_list

    def getPageDom(self) -> str:
        return self._page_dom

    def getFormXPath(self) -> str:
        return self._form_xpath
