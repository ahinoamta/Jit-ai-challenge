# Docker Script Wrapper with LLM

This tool leverages Language Models to automatically generate Dockerfiles for CLI scripts. After generating the Dockerfile, it builds the image and runs it according to the example usage defined in the provided README. The design supports multiple LLM providers through a pluggable interface.

## Features

- Automatically generates Dockerfiles for CLI scripts
- Supports multiple programming languages (Python, JavaScript, Bash, etc.)
- Verifies the Docker container output against expected results by extracting the example usage from the script's README
- Extensible LLM provider system (currently supports OpenAI)
- Basic sanitization and prompt injection detection

## Installation

1. Clone the repository
2. Install requirments:
```bash
pip install -r requirements.txt
```
3. Set up your environment:
   - Set OPENAI_API_KEY in your environment, or
   - Provide it via the --api-key argument

## Usage

Basic usage:
```bash
python main.py --script <path_to_script> --llm <llm_provider> --api-key <your_api_key>
```

Arguments:
- `--script`: Path to the script you want to wrap in Docker (required)
- `--llm`: LLM provider to use (default: 'openai')
- `--api-key`: API key for the LLM service (optional if set in environment)

Example:
```bash
python main.py --script ./scripts/word_reverser/word_reverser.py --llm openai --api-key your-api-key
```

## How It Works

1. The tool reads your script and its README
2. Uses LLM to generate an appropriate Dockerfile
3. Builds the Docker image
4. Extracts example usage from README
5. Runs the container with the example input
6. Verifies the output matches the expected result

## Adding a New Script

1. Create a new directory under `scripts/` with your script name:
```bash
mkdir scripts/my_script
```

2. Add your script file (e.g., `my_script.py`, `my_script.js`, etc.)

3. Create a README file named `README_my_script.md` with:
   - Description of what the script does
   - Requirements
   - Usage instructions
   - Example command with expected output:
```markdown
## Example

\`\`\`bash
python my_script.py 'input text'
\`\`\`

Output:
\`\`\`
expected output
\`\`\`
```

## Adding a New LLM Provider

1. Create a new client class implementing `LLMClientInterface`:
```python
from llm_clients.llm_client_interface import LLMClientInterface

class MyLLMClient(LLMClientInterface):
    def get_structured_response(self, user_prompt: str, system_prompt: str, 
                              response_format: type[T], model: str = None, 
                              max_tokens: int = 300) -> T:
        # Implement structured response logic
        pass

    def get_response(self, user_prompt: str, system_prompt: str, 
                    model: str = None, max_tokens: int = 300) -> str:
        # Implement raw text response logic
        pass
```

2. Add the new provider to `LLMType` enum in `services/llm_resolver.py`:
```python
class LLMType(Enum):
    OPENAI = "openai"
    MY_LLM = "my-llm"  # Add your new LLM type
```

3. Update the `resolve` method in `LLMResolver`:
```python
if llm == LLMType.MY_LLM:
    return MyLLMClient(api_key)
```

4. Use your new provider:
```bash
python main.py --script ./my_script.py --llm my-llm --api-key your-api-key
```

## Directory Structure

```
.
├── main.py                    # Main script
├── services/
│   ├── dockerfile_generator.py # Generates Dockerfiles
│   ├── docker_manager.py      # Manages Docker operations
│   ├── llm_resolver.py        # Resolves LLM clients
│   └── readme_content_extractor.py # Extracts info from 
├── llm_clients/
│   ├── llm_client_interface.py # Abstract interface for LLM
│   └── openai_client.py       # OpenAI implementation
└── scripts/                   # Your scripts go here
    └── example_script/
        ├── example_script.py
        └── README_example_script.md
```
