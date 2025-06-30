#!/usr/bin/env python3
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.TestCombinationOutputResponse import TestCombinationOutputResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import GoogleAPIError
import os

# Google API Key
DEFAULT_GOOGLE_API_KEY = "****"

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = DEFAULT_GOOGLE_API_KEY


class Gemini(ILlmService):
    llm = None
    structured_llm = None

    def __init__(self, model_name="gemini-2.5-pro", temperature=0):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
        )
        self.structured_llm = self.llm.with_structured_output(TestCombinationOutputResponse)

    def get_response(self, prompt: str, **kwargs) -> str:
        # TODO: Improve prompt, maybe add system_prompt, etc...
        try:
            response = self.llm.invoke(prompt)
            if response is not None:
                return response.content
        except GoogleAPIError:
            return None

    def get_structured_response(self, prompt: str, **kwargs):
        # TODO: Improve prompt, maybe add system_prompt, etc...
        try:
            response = self.structured_llm.invoke(prompt)
            if response is not None:
                return response
        except GoogleAPIError:
            return None
