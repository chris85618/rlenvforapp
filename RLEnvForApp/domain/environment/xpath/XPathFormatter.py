import re

class XPathFormatter:
    @staticmethod
    def format(xpath: str) -> str:
        def _add_index(match):
            tag = match.group(1)
            pred = match.group(2)
            # 若節點沒有 predicate 則加上 [1]
            if not pred:
                return f'/{tag}[1]'
            # 否則保留原索引
            return f'/{tag}{pred}'
        result_xpath = re.sub(r'/([a-zA-Z_][\w\-]*)(\[[^\]]*\])?', _add_index, xpath)
        return result_xpath
