from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar('T')

class LLMClientInterface(ABC):
    @abstractmethod
    def get_structured_response(self, user_prompt: str, system_prompt: str, response_format: type[T], model: str = None, max_tokens: int = 300) -> T:
        """
        Get a structured response from the LLM
        Args:
            user_prompt: The prompt to send to the LLM
            system_prompt: The system message that sets the context
            response_format: The type to parse the response into
            model: The model to use (optional)
            max_tokens: Maximum tokens in the response
        Returns:
            The parsed response in the specified format
        """
        pass

    @abstractmethod
    def get_response(self, user_prompt: str, system_prompt: str, model: str = None, max_tokens: int = 300) -> str:
        """
        Get a raw text response from the LLM
        Args:
            user_prompt: The prompt to send to the LLM
            system_prompt: The system message that sets the context
            model: The model to use (optional)
            max_tokens: Maximum tokens in the response
        Returns:
            The raw text response
        """
        pass
