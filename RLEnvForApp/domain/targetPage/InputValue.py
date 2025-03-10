from RLEnvForApp.domain.targetPage.Dom import Dom


class InputValue:
    action:int = None
    xpath:str = ""
    value:str = ""

    def __init__(self, xpath:str, value:str, action=None):
        self.xpath = xpath
        self.value = value
        self.action = action
    
    def getXpath(self):
        return self.xpath
    
    def getValue(self):
        return self.value
    
    def getAction(self):
        return self.action
