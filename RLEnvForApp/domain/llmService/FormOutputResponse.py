from typing import List
from typing_extensions import Annotated, TypedDict
from RLEnvForApp.domain.llmService.TestFieldOutputResponse import TestFieldOutputResponse


class FormOutputResponse(TypedDict):
    test_combination_list: Annotated[List[TestFieldOutputResponse], "List of test fields input strings."]
