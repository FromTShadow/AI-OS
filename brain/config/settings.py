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

OLLAMA_CONTEXT_WINDOW = 4096
DEFAULT_CHAT_MAX_TOKENS = 700
DEFAULT_CHAT_TIMEOUT_SECONDS = 180
PIPELINE_CHAT_TIMEOUT_SECONDS = 300

ROLE_MAX_TOKENS = {
    "research": 1400,
    "developer": 1200,
    "trading": 1200,
    "second_brain": 1000,
    "ceo": 900,
    "general": 900,
}

# ======================================================
# PLANNER
# ======================================================

PLANNER_MODE = "deterministic"

LLM_PLANNER_MODEL = "qwen3.5:4b"

LLM_PLANNER_MAX_ATTEMPTS = 2

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