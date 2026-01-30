import ollama
from typing import List, Generator, Any
from zeta.utils.logger import logger
from zeta.core.system.config_manager import ConfigManager

class ModelManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.host = self.config.get("llm.host", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)
        self.current_model = self.config.get("llm.model", "llama3:8b")

    def list_models(self) -> List[str]:
        try:
            models = self.client.list()
            return [m['name'] for m in models['models']]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def check_connection(self) -> bool:
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def pull_model(self, model_name: str):
        logger.info(f"Pulling model: {model_name}...")
        try:
            progress = self.client.pull(model_name, stream=True)
            for p in progress:
                # In a real CLI we'd show a progress bar
                pass 
            logger.info(f"Model {model_name} pulled successfully.")
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")

    def generate(self, prompt: str, model: str = None, stream: bool = True) -> Generator[str, None, None]:
        target_model = model or self.current_model
        logger.debug(f"Generating with model: {target_model}")
        try:
            response = self.client.generate(model=target_model, prompt=prompt, stream=stream)
            if stream:
                for chunk in response:
                    yield chunk['response']
            else:
                yield response['response']
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            yield f"Error: {str(e)}"
