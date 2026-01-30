from datetime import datetime
from zeta.core.tools.file_manager import FileManager
from zeta.core.memory.memory_manager import MemoryManager
from zeta.utils.logger import logger

class NoteTaker:
    def __init__(self, file_manager: FileManager, memory_manager: MemoryManager):
        self.fm = file_manager
        self.mem = memory_manager
        
        # Ensure notes directory exists
        if not (self.fm.workspace_root / "notes").exists():
            (self.fm.workspace_root / "notes").mkdir()

    def create_note(self, title: str, content: str) -> str:
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notes/{safe_title}_{timestamp}.md"
        
        full_content = f"# {title}\nDate: {datetime.now()}\n\n{content}"
        
        if self.fm.write_file(filename, full_content):
            # Also index this in memory for retrieval
            self.mem.save_interaction(f"Archive note: {title}", content)
            return f"Note saved to {filename}"
        else:
            return "Failed to save note."

    def list_notes(self) -> str:
        files = self.fm.list_directory("notes")
        return "\n".join(files) if files else "No notes found."
