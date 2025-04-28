from pydantic import BaseModel, Field


class TestFieldOutputResponse(BaseModel):
    xpath: str = Field(
        ...,
        description="The XPath of the given field.",
        example="//input[@name='username']"
    )
    action_number: int = Field(
        ...,
        description="Action number for the given field between -1, 0, and 1.",
        example=1
    )
    input_value: str = Field(
        ...,
        description="Input value for the given field.",
        example="test_user"
    )

    def to_xpath_dict(self) -> dict:
        """
        Convert the TestFieldOutputResponse to a dictionary with the XPath as the key.
        """
        return {
            self.xpath: {
                "action_number": self.action_number,
                "input_value": self.input_value
            }
        }
