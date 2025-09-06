from pydantic import BaseModel

class ReadmeContentEvent(BaseModel):
    example_command_args: str
    expected_output: str

class ReadmeContentExtractor:
    SYSTEM_PROMPT = "You are a helpful assistant that extracts structured data from documentation."

    def __init__(self, llm_client):
        self.client = llm_client

    def extract(self, readme_path) -> ReadmeContentEvent:
        with open(readme_path, 'r') as f:
            readme_content = f.read()
            
        prompt = f"""
        Given the following README file, extract:
        1. The arguments of the first example usage command - no explanation, no markdown, just the command arguments. If there are no arguments, return an empty string. If there are multilines arguments, keep them with line breaks.
        2. The expected output for that example (as a single line or block, no explanation, no markdown, just the output).
    
        README:
        {readme_content}
        """
    
        event = self.client.get_structured_response(
            user_prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            response_format=ReadmeContentEvent
        )

        return event
