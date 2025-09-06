from enum import Enum
from typing import Optional
from llm_clients.llm_client_interface import LLMClientInterface
from llm_clients.openai_client import OpenAIClient

class LLMType(Enum):
    OPENAI = "openai"
    # Add more LLM types here as they become available
    # For example:
    # ANTHROPIC = "anthropic"
    # GOOGLE = "google"

class LLMResolver:
    @staticmethod
    def resolve(llm_type: str, api_key: str) -> LLMClientInterface:
        """
        Resolves and returns the appropriate LLM client based on the specified type
        Args:
            llm_type: The type of LLM to use (from LLMType enum)
            api_key: API key for the LLM service
        Returns:
            An instance of LLMClientInterface
        Raises:
            ValueError: If the specified LLM type is not supported
        """
        try:
            llm = LLMType(llm_type.lower())
        except ValueError:
            supported_types = [t.value for t in LLMType]
            raise ValueError(f"Unsupported LLM type: {llm_type}. Supported types are: {supported_types}")

        if llm == LLMType.OPENAI:
            try:
                return OpenAIClient(api_key)
            except Exception as e:
                raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
        
        # Add more LLM implementations here as they become available
        # elif llm == LLMType.ANTHROPIC:
        #     return AnthropicClient(api_key)
        
        raise ValueError(f"Implementation not found for LLM type: {llm_type}")
