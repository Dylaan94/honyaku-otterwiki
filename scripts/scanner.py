"""
Simple scanner: reads all files from a target directory and compares
against existing wiki docs to find what's new and needs documentation.
"""

from pathlib import Path


def scan_directory(target_dir: str, extensions: list[str] | None = None) -> list[dict]:
    """
    Recursively read all files in a directory.

    Args:
        target_dir: Path to the directory to scan.
        extensions: Optional list of file extensions to include (e.g. [".query", ".task"]).
                    If None, includes all files.

    Returns:
        List of dicts with keys: name, slug, path, content, subfolder.
        subfolder is "apis" or "tasks" based on parent directory name.
    """
    target = Path(target_dir).resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"Directory not found: {target}")

    files = []
    for filepath in sorted(target.rglob("*")):
        if not filepath.is_file():
            continue
        if filepath.name.startswith("."):
            continue
        if extensions and filepath.suffix not in extensions:
            continue

        content = filepath.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            continue

        # Determine category from parent folder name
        relative = filepath.relative_to(target)
        parts = relative.parts
        subfolder = _classify(parts, content)

        slug = filepath.stem.replace(" ", "-").lower()

        files.append({
            "name": filepath.stem,
            "slug": slug,
            "path": str(filepath),
            "relative_path": str(relative),
            "content": content,
            "subfolder": subfolder,
        })

    return files


def _classify(path_parts: tuple, content: str) -> str:
    """Determine if a file is an API or a task based on folder name or content."""
    folder_hint = "/".join(path_parts[:-1]).lower()

    if "api" in folder_hint or "endpoint" in folder_hint or "route" in folder_hint:
        return "apis"
    if "task" in folder_hint or "command" in folder_hint or "job" in folder_hint:
        return "tasks"

    # Fall back to content sniffing
    first_line = content.strip().split("\n")[0].lower()
    if "query" in first_line and ("verb=" in first_line or "api" in first_line):
        return "apis"
    if "task" in first_line or "command" in first_line or "schedule" in first_line:
        return "tasks"

    # Default
    return "apis"


def get_existing_docs(wiki_dir: str) -> dict[str, set[str]]:
    """Return sets of existing doc slugs for each subfolder."""
    wiki = Path(wiki_dir)
    result = {}
    for subfolder in ["apis", "tasks"]:
        folder = wiki / subfolder
        if folder.exists():
            result[subfolder] = {f.stem for f in folder.glob("*.md")}
        else:
            result[subfolder] = set()
    return result
