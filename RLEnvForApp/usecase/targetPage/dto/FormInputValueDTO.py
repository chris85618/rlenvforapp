from RLEnvForApp.usecase.targetPage.dto.InputValueDTO import InputValueDTO


class FormInputValueDTO:
    def __init__(self, inputValueListDto: [InputValueDTO], page_dom: str, form_xpath: str):
        self._inputValueListDto = inputValueListDto
        self._page_dom = page_dom
        self._form_xpath = form_xpath

    def getInputValueListDto(self) -> [InputValueDTO]:
        return self._inputValueListDto

    def getPageDom(self) -> str:
        return self._page_dom

    def getFormXPath(self) -> str:
        return self._form_xpath
