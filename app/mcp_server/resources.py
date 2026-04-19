from pathlib import Path


def load_architecture_markdown() -> str:
    architecture_path = Path(__file__).resolve().parents[2] / "ARCHITECTURE.md"
    return architecture_path.read_text(encoding="utf-8")
