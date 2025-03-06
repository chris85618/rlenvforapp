from RLEnvForApp.domain.targetPage.Dom import Dom


class InputValue:
    xpath:str = ""
    value:str = ""

    def __init__(self, xpath:str, value:str):
        self.xpath = xpath
        self.value = value
    
    def getXpath(self):
        return self.xpath
    
    def getValue(self):
        return self.value
