"""
Prompt loader for AI-OS.

Loads prompt content and YAML-style front matter from Markdown files.
Prompt behavior remains separate from Python execution logic.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from brain.config.settings import AI_OS_ROOT


class PromptNotFoundError(FileNotFoundError):
    """Raised when a requested AI-OS prompt does not exist."""


@dataclass(frozen=True)
class PromptDocument:
    name: str
    version: str
    description: str
    content: str
    path: Path


class PromptLoader:
    def __init__(self, prompt_directory: Optional[Path] = None):
        self.prompt_directory = (
            prompt_directory
            if prompt_directory is not None
            else AI_OS_ROOT / "brain" / "prompts"
        )

    def available_prompts(self) -> List[str]:
        if not self.prompt_directory.exists():
            return []

        return sorted(
            path.stem
            for path in self.prompt_directory.glob("*.md")
        )

    def prompt_path(self, name: str) -> Path:
        normalized_name = name.strip().lower().replace("-", "_")
        return self.prompt_directory / f"{normalized_name}.md"

    def parse_front_matter(self, text: str) -> tuple:
        """
        Parse simple YAML-style front matter without requiring PyYAML.
        """
        if not text.startswith("---\n"):
            return {}, text.strip()

        closing_marker = text.find("\n---\n", 4)

        if closing_marker == -1:
            raise ValueError("Prompt front matter is not closed correctly.")

        metadata_text = text[4:closing_marker]
        content = text[closing_marker + 5:].strip()

        metadata: Dict[str, str] = {}

        for line in metadata_text.splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

        return metadata, content

    def load_document(self, name: str) -> PromptDocument:
        path = self.prompt_path(name)

        if not path.is_file():
            raise PromptNotFoundError(
                f"Prompt '{name}' was not found at: {path}"
            )

        raw_text = path.read_text(encoding="utf-8").strip()

        if not raw_text:
            raise ValueError(f"Prompt '{name}' is empty.")

        metadata, content = self.parse_front_matter(raw_text)

        if not content:
            raise ValueError(f"Prompt '{name}' has no prompt content.")

        return PromptDocument(
            name=metadata.get("name", path.stem),
            version=metadata.get("version", "unversioned"),
            description=metadata.get("description", ""),
            content=content,
            path=path,
        )

    def load(self, name: str) -> str:
        return self.load_document(name).content

    def load_bundle(self, specialist: str) -> Dict[str, PromptDocument]:
        return {
            "system": self.load_document("system"),
            "specialist": self.load_document(specialist),
        }