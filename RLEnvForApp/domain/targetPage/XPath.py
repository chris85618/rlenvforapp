# TODO: Replace all the origin XPath (string) into this data structure

class XPath:
    _xpath = ""

    def __init__(self, xpath: str):
        self._xpath = xpath

    def get(self) -> Dom:
        return self._xpath
