from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
from RLEnvForApp.domain.llmService.FormOutputResponse import FormOutputResponse


class HighLevelAction:
    app_event_dict: {str, AppEvent} = {}
    page_dom:str=""

    def __init__(self, *app_event_list: list[AppEvent], page_dom: str = "", form_xpath: str = ""):
        self.app_event_dict = {}
        formatted_form_xpath = XPathFormatter.format(form_xpath)
        self.form_xpath = formatted_form_xpath

        self.page_dom = page_dom

        for app_event in app_event_list:
            self.append(app_event)
    
    @classmethod
    def fromFormOutputResponse(cls, form_output_response: FormOutputResponse, page_dom: str = "", form_xpath: str = ""):
        app_event_list = [AppEvent.fromTestFieldOutputResponse(test_field_output_response)
                            for test_field_output_response in form_output_response.test_combination_list]
        return cls(*app_event_list, page_dom=page_dom, form_xpath=form_xpath)
    
    @classmethod
    def fromHighLevelAction(cls, high_level_action):
        form_xpath = high_level_action.form_xpath
        app_event_list = high_level_action.getAppEventList()
        page_dom = high_level_action.page_dom
        return cls(*app_event_list, page_dom=page_dom, form_xpath=form_xpath)

    def append(self, app_event: AppEvent):
        xpath = app_event.getXpath()
        formatted_xpath = XPathFormatter.format(xpath)
        self.app_event_dict[formatted_xpath] = app_event

    def update(self, new_page_dom: str, updated_app_event_dict: dict[str, AppEvent]):
        # Update the page DOM if it has changed
        self.page_dom = new_page_dom
        # Update the input value dictionary with new values
        for xpath, app_event in updated_app_event_dict.items():
            formatted_xpath = XPathFormatter.format(xpath)
            self.app_event_dict[formatted_xpath] = app_event

    def getFormXPath(self) -> str:
        return self.form_xpath

    def getPageDom(self) -> str:
        return self.page_dom

    def getAppEventList(self) -> list[AppEvent]:
        return self.app_event_dict.values()
    
    def getAppEventByXpath(self, xpath:str) -> AppEvent:
        formatted_xpath = XPathFormatter.format(xpath)
        return self.app_event_dict.get(formatted_xpath)
    
    def getAppEventDict(self) -> dict:
        return self.app_event_dict
    
    def toString(self) -> str:
        result = ""
        for xpath, app_event in self.app_event_dict.items():
            value = app_event.getValue()
            category = app_event.getCategory()
            result += f"xpath: {xpath}, value: {value}, category: {category}\n"
        return result
