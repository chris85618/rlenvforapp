from RLEnvForApp.domain.environment.actionCommandFactoryService.defaultValue.IDefaultValue import IDefaultValue
from RLEnvForApp.domain.environment.xpath.XPathFormatter import XPathFormatter
import os
import json

class DefaultValueJsonFetcher(IDefaultValue):
    data = {}

    def set_aut_name(self, aut_name: str):
        super().set_aut_name(aut_name)
        if os.path.exists("default_value.json"):
            with open("default_value.json", "r") as json_file:
                new_data = {}
                json_data = json.load(json_file)
                app_data = json_data[aut_name]
                # Format XPaths
                for url, value_dict in app_data.items():
                    new_input_value = {}
                    for xpath, value_dict in value_dict.items():
                        formatted_xpath = XPathFormatter.format(xpath)
                        value = value_dict["value"]
                        new_input_value[formatted_xpath] = value
                    new_data[url] = new_input_value

                self.data = new_data

    def get_xpath_default_value_dict(self, url:str) -> dict[str, str]:
        if url in self.data:
            xpath_input_value_mapping_table = self.data[url]
            return xpath_input_value_mapping_table
        return None

    def get_default_value(self, url:str, xpath:str) -> str:
        if url in self.data:
            xpath_input_value_mapping_table = self.data[url]

            formatted_xpath = XPathFormatter.format(xpath)

            if formatted_xpath in xpath_input_value_mapping_table:
                return xpath_input_value_mapping_table[formatted_xpath]
        return None
    
    def in_default_value(self, url:str, xpath:str) -> bool:
        if url in self.data:
            xpath_input_value_mapping_table = self.data[url]

            formatted_xpath = XPathFormatter.format(xpath)

            if formatted_xpath in xpath_input_value_mapping_table:
                return True
        return False
