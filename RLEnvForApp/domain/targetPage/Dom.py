from lxml import etree
from io import StringIO

# TODO: Replace all the origin DOM (string) into this data structure


class Dom:
    _dom = None

    def __init__(self, dom):
        if isinstance(dom, str):
            self._dom = etree.parse(StringIO(dom), etree.HTMLParser())
        elif isinstance(dom, etree._Element):
            self._dom = dom
        else:
            raise

    def tostring(self, pretty_print=False, method="html", encoding="unicode", **xargs) -> str:
        return etree.tostring(self._dom, pretty_print=pretty_print, method=method, encoding=encoding, **xargs)

    def getByXpath(self, xpath: str, index=0):
        return Dom(self._dom.xpath(xpath)[index])
