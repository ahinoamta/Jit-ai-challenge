class DockerfileGenerator:
    SYSTEM_PROMPT = """
    You are a Docker expert. You generate minimal Dockerfiles to run scripts.
    Rules:
    - Detect the script language from file extension or shebang.
    - Include only what is needed to run the script.
    - Assume Ubuntu base images unless language-specific images are better.
    - Copy the script into the container and set CMD/ENTRYPOINT.
    - The DockerFile is located in the same directory as the script.
    - Build the docker file in a way that the user can run it with: docker run <image_name> <script_arguments>.
    - <image_name> should be the script name (according to the script path without the extension), and the <script_arguments> should be as the example usage.
    - Use the full script path to avoid missing files.
    Always output ONLY the raw Dockerfile text. 
    Do not include explanations, formatting, markdown, or code fences.
    """
        
    def __init__(self, llm_client):
        self.client = llm_client

    def generate(self, script_path, readme_path, output_path="Dockerfile"):        
        prompt = f"""
        Given the following script and README, generate a Dockerfile that will run this script correctly.

        Script path: {script_path}
        README content: {readme_path}

        Please follow the rules in the system prompt, as well as the requirements and the example usage in the README file.
        """

        dockerfile_content = self.client.get_response(
            user_prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT
        )
        
        with open(output_path, 'w') as f:
            f.write(dockerfile_content)
        return output_path
