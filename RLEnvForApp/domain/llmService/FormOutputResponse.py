from typing import List
from pydantic import BaseModel
from RLEnvForApp.domain.llmService.TestFieldOutputResponse import TestFieldOutputResponse

class FormOutputResponse(BaseModel):
    test_combination_list: List[TestFieldOutputResponse]
