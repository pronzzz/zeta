import os
from zeta.utils.logger import logger

class SystemTool:
    def list_dir(self, path: str = ".") -> str:
        """Lists files in the specified directory."""
        try:
            return str(os.listdir(path))
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    def read_file(self, path: str) -> str:
        """Reads the content of a file."""
        if not os.path.exists(path):
            return "File not found."
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
