from typing import TypeVar
from .llm_client_interface import LLMClientInterface
from openai import OpenAI
import os

T = TypeVar('T')

class OpenAIClient(LLMClientInterface):
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)

    def get_structured_response(self, user_prompt: str, system_prompt: str, response_format: type[T], model: str = "gpt-4o-2024-08-06", max_tokens: int = 300) -> T:
        response = self.client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            response_format=response_format
        )
        return response.choices[0].message.parsed
    
    def get_response(self, user_prompt: str, system_prompt: str, model: str = "gpt-4.1-mini", max_tokens: int = 300) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
