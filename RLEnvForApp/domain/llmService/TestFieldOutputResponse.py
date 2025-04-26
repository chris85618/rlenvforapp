from typing_extensions import Annotated, TypedDict


class TestFieldOutputResponse(TypedDict):
    xpath: Annotated[str, "The XPath of the given field."]
    action_number: Annotated[int, "Action number for the given field between -1, 0, and 1."]
    input_value: Annotated[str, "Input value for the given field."]
    
    def to_xpath_dict(self) -> dict:
        """
        Convert the TestFieldOutputResponse to a dictionary with the XPath as the key.
        """
        return {self.xpath: {"action_number": self.action_number, "input_value": self.input_value}}
