import subprocess
import shlex

class DockerManager:
    def __init__(self, dockerfile_path="Dockerfile"):
        self.dockerfile_path = dockerfile_path

    def build_image(self, tag="wrapped-script:latest"):
        cmd = ["docker", "build", "-f", self.dockerfile_path, "-t", tag, "."]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr

    def run_container(self, tag="wrapped-script:latest", command=None):
        cmd = ["docker", "run", "--rm", tag]
        if command:
            # If command is a string, split by spaces, but preserve quoted arguments
            cmd += shlex.split(command)
            print(f"Command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
