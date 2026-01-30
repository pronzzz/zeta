from zeta.core.llm.model_manager import ModelManager
from zeta.core.tools.file_manager import FileManager
from zeta.utils.logger import logger
from typing import Generator

class Summarizer:
    def __init__(self, model_manager: ModelManager, file_manager: FileManager):
        self.mm = model_manager
        self.fm = file_manager

    def summarize_text(self, text: str) -> Generator[str, None, None]:
        prompt = f"""
        Please provide a concise summary of the following text:
        
        {text[:10000]}  # Truncate to safe limit for now
        
        Summary:
        """
        yield from self.mm.generate(prompt)

    def summarize_file(self, filename: str) -> Generator[str, None, None]:
        content = self.fm.read_file(filename)
        if not content:
            yield f"Error: Could not read file {filename}"
            return
            
        yield f"Summary of {filename}:\n"
        yield from self.summarize_text(content)
