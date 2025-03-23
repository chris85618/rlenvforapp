from lxml import etree
from io import StringIO

# TODO: Replace all the origin DOM (string) into this data structure


class Dom:
    _dom = ""

    def __init__(self, dom:str):
        if dom is str:
            self._dom = etree.parse(StringIO(dom), etree.HTMLParser())
        elif dom is etree.ElementTree:
            self._dom = dom
        else:
            raise

    def tostring(self, pretty_print=False, method="html", encoding="unicode", **xargs) -> str:
        return etree.tostring(self._dom.tostring(), pretty_print=pretty_print, method=method, encoding=encoding, **xargs)

    def getByXpath(self, xpath: str):
        return Dom(self._dom.xpath(xpath))
