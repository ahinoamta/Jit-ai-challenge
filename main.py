import argparse
import os
import sys
from services.dockerfile_generator import DockerfileGenerator
from services.docker_manager import DockerManager
from services.llm_resolver import LLMResolver, LLMType
from services.readme_content_extractor import ReadmeContentExtractor
from services.utils import sanitize_input, is_prompt_injection

def main():
    parser = argparse.ArgumentParser(description="Wrap a script in a Dockerfile using OpenAI API.")
    parser.add_argument('--script', required=True, help='Path to the script to wrap')
    parser.add_argument('--llm', default='openai', help=f'LLM service to use. Available options: {[t.value for t in LLMType]}')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env variable)')
    args = parser.parse_args()

    script_path = sanitize_input(args.script)
    script_dir_name = os.path.basename(os.path.dirname(script_path))
    readme_path = os.path.dirname(script_path) + "/README_" + script_dir_name + ".md"
    output_path = os.path.dirname(script_path) + "/Dockerfile_" + script_dir_name + ".Dockerfile"

    if is_prompt_injection(script_path):
        print("❌ Potential prompt injection detected. Aborting.")
        return
    
    try:
        llm_client = LLMResolver.resolve(args.llm, args.api_key)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    dockerfile_generator = DockerfileGenerator(llm_client)
    dockerfile_path = dockerfile_generator.generate(script_path, readme_path, output_path)
    print(f"📄 Dockerfile created: {dockerfile_path}")

    docker_manager = DockerManager(dockerfile_path)
    print(f"🔨 Building Docker image: {script_dir_name}")
    success, build_log = docker_manager.build_image(tag=script_dir_name)
    print(f"🛠️ Build log: {build_log}")
    if not success:
        print("❌ Docker build failed.")
        # TODO: add a retry mechanism for re-generating the Dockerfile
        return
    
    print("📖 Extracting example command and expected output from README...")
    readme_content_extractor = ReadmeContentExtractor(llm_client)
    content = readme_content_extractor.extract(readme_path)
    if not content.example_command_args or not content.expected_output:
        print("❌ Could not extract example command args or expected output from README using OpenAI.")
        return

    print("▶️ Running container test:")
    success, run_log = docker_manager.run_container(tag=script_dir_name, command=content.example_command_args)
    print(f"📦 Container output: {run_log}")
    if not success:
        print("❌ Container run failed.")
        return

    # Assert output matches expected
    if content.expected_output.strip() == run_log.strip():
        print("✅ Test passed — output matches the expected result from README.")
        print("🚀 Your script is now containerized and can be run safely using the generated Dockerfile.")
        sys.exit(0)
    else:
        print("❌ Test failed — output does not match expected output from README. Try to run the script again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
