"""
AI-OS Global Configuration
Single source of truth for the Brain.
"""

from pathlib import Path

# ======================================================
# PATHS
# ======================================================

HOME = Path.home()

AI_OS_ROOT = HOME / "AI-OS"

VAULT_PATH = AI_OS_ROOT / "vault"

PROJECTS_PATH = AI_OS_ROOT / "projects"

DATABASE_PATH = AI_OS_ROOT / "databases"

BACKUP_PATH = AI_OS_ROOT / "backups"

LOG_PATH = AI_OS_ROOT / "logs"

# ======================================================
# OLLAMA
# ======================================================

OLLAMA_URL = "http://localhost:11434"

CHAT_MODEL = "qwen3:14b"

EMBED_MODEL = "nomic-embed-text"

# ======================================================
# QDRANT
# ======================================================

QDRANT_HOST = "localhost"

QDRANT_PORT = 6333

COLLECTION_NAME = "obsidian_memory"

VECTOR_SIZE = 768

# ======================================================
# POSTGRES
# ======================================================

POSTGRES_HOST = "localhost"

POSTGRES_PORT = 5432

# ======================================================
# OPEN WEBUI
# ======================================================

OPENWEBUI_URL = "http://localhost:3000"

# ======================================================
# BRAIN
# ======================================================

BRAIN_NAME = "AI Brain"

VERSION = "0.1"