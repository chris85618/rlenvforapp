class IDefaultValue:
    aut_name = None

    def set_aut_name(self, aut_name: str):
        self._aut_name = aut_name

    def get_default_value(self, url:str, xpath:str) -> str:
        """
        Returns the default value.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_xpath_default_value_dict(self, url:str) -> dict[str, str]:
        """
        Returns the default values list.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def in_default_value(self, url:str, xpath:str) -> bool:
        """
        Returns True if the xpath is in the default value.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def any_in_default_value(self, url:str, *xpath_list:str) -> bool:
        for xpath in xpath_list:
            if self.in_default_value(url, xpath):
                return True
        return False
