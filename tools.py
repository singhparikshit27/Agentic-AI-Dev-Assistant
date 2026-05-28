# tools.py
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

# --- Tool 1: Code/File Writer ---
class FileWriteSchema(BaseModel):
    """Input schema for the WriteFileTool."""
    filename: str = Field(description="The full path and name of the file to write (e.g., 'app.py', 'src/data.py').")
    content: str = Field(description="The full content (text or code) that should be written to the file.")

class WriteFileTool(BaseTool):
    name: str = "Code/File Writer Tool"
    description: str = (
        "Useful for creating new files or overwriting existing files with new code, "
        "configurations, or any text content. It takes the full file path and the complete content."
    )
    args_schema: Type[BaseModel] = FileWriteSchema

    def _run(self, filename: str, content: str) -> str:
        """The actual code that runs when the LLM calls the tool."""
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            with open(filename, 'w') as f:
                f.write(content)
            return f"File successfully written: '{filename}' (size: {len(content)} characters)."
        except Exception as e:
            return f"Error writing file '{filename}': {e}"


# --- Tool 2: File Reader ---
class FileReadSchema(BaseModel):
    """Input schema for the ReadFileTool."""
    filename: str = Field(description="The full path and name of the file to read.")

class ReadFileTool(BaseTool):
    name: str = "File Reader Tool"
    description: str = (
        "Useful for reading the content of an existing file for review, debugging, "
        "or checking existing code. Input is the full file path."
    )
    args_schema: Type[BaseModel] = FileReadSchema

    def _run(self, filename: str) -> str:
        """The actual code that runs when the LLM calls the tool."""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return f"Content of '{filename}':\n\n{content[:200]}..." 
        except FileNotFoundError:
            return f"Error: File not found at path '{filename}'."
        except Exception as e:
            return f"Error reading file '{filename}': {e}"


file_writer_tool = WriteFileTool()
file_reader_tool = ReadFileTool()

AVAILABLE_TOOLS = [file_writer_tool, file_reader_tool]