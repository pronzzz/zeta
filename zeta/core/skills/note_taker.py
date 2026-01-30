import os
from zeta.utils.logger import logger

class NoteTaker:
    NOTES_DIR = "./workspace/notes"

    def __init__(self):
        os.makedirs(self.NOTES_DIR, exist_ok=True)

    def create_note(self, title: str, content: str) -> str:
        """Creates a new note with the given title and content."""
        filename = f"{title.replace(' ', '_')}.md"
        path = os.path.join(self.NOTES_DIR, filename)
        
        try:
            with open(path, "w") as f:
                f.write(content)
            logger.info(f"Created note: {filename}")
            return f"Note created successfully at {path}"
        except Exception as e:
            return f"Failed to create note: {str(e)}"

    def read_note(self, title: str) -> str:
        """Reads a note by title (or filename)."""
        if not title.endswith(".md"):
            title += ".md"
        path = os.path.join(self.NOTES_DIR, title)
        
        if not os.path.exists(path):
            return "Note not found."
            
        with open(path, "r") as f:
            return f.read()

    def list_notes(self) -> str:
        """Lists all available notes."""
        files = os.listdir(self.NOTES_DIR)
        return "\n".join(files) if files else "No notes found."
