class InputValueEntity:
    def __init__(self, xpath: str, value: str, action: int):
        self._xpath = xpath
        self._value = value
        self._action = action

    def getXpath(self) -> str:
        return self._xpath
    
    def getValue(self) -> str:
        return self._value
    
    def getAction(self) -> int:
        return self._action
