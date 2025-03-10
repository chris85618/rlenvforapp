class InputValuePool:
    pool:dict = {}

    def add(self, url:str, xpath:str, input_value:str):
        self.pool[self._getIndex(url, xpath)] = input_value

    def get(self, url:str, xpath:str) -> str:
        return self.pool.get(self._getIndex(url, xpath))

    def _getIndex(self, url:str, xpath:str) -> tuple:
        return tuple(url, xpath)
