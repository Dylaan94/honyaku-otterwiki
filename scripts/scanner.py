"""
Scanner: reads files from specific folders in a Xanoscript project and
compares against existing wiki docs to find what needs documentation.
Preserves subfolder structure (e.g. apis/docling/, apis/llm/).
"""

from pathlib import Path

# Top-level folders in the Xano project that we scan.
SCAN_FOLDERS = [
    "apis",
    "functions",
    "agents",
    "mcp_servers",
    "middlewares",
    "tables",
    "tasks",
]


def scan_project(target_dir: str, folders: list[str] | None = None) -> list[dict]:
    """
    Scan specific folders in a Xanoscript project for files to document.
    Preserves subfolder structure within each top-level folder.

    Args:
        target_dir: Root path of the Xanoscript project.
        folders: Which top-level folders to scan (default: all SCAN_FOLDERS).

    Returns:
        List of dicts with keys: name, slug, path, relative_path, content, category, wiki_path.
        wiki_path is the full subfolder path for the doc (e.g. "apis/docling").
    """
    target = Path(target_dir).resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"Directory not found: {target}")

    folders_to_scan = folders or SCAN_FOLDERS
    files = []

    for folder in folders_to_scan:
        folder_path = target / folder
        if not folder_path.exists():
            print(f"  [skip] {folder}/ not found in project")
            continue

        for filepath in sorted(folder_path.rglob("*")):
            if not filepath.is_file():
                continue
            if filepath.name.startswith("."):
                continue
            if filepath.name == "triggers":
                continue

            content = filepath.read_text(encoding="utf-8", errors="replace")
            if not content.strip():
                continue

            # Build the wiki path preserving subfolders
            # e.g. apis/docling/1035_test_POST.xs -> wiki_path="apis/docling", slug="1035_test_post"
            relative_to_folder = filepath.relative_to(folder_path)
            parent_parts = relative_to_folder.parent.parts  # subfolder(s) within the top-level folder

            if parent_parts:
                wiki_path = f"{folder}/{'/'.join(parent_parts)}"
            else:
                wiki_path = folder

            slug = filepath.stem.replace(" ", "-").lower()

            files.append({
                "name": filepath.stem,
                "slug": slug,
                "path": str(filepath),
                "relative_path": str(filepath.relative_to(target)),
                "content": content,
                "category": folder,
                "wiki_path": wiki_path,
            })

    return files


def get_existing_docs(wiki_dir: str) -> set[str]:
    """
    Return a set of existing doc identifiers (wiki_path/slug) across all folders.
    e.g. {"apis/docling/1035_test_post", "apis/llm/462_translation_memory_get"}
    """
    wiki = Path(wiki_dir)
    existing = set()
    for md_file in wiki.rglob("*.md"):
        relative = md_file.relative_to(wiki)
        # Build the identifier: parent_path/stem
        identifier = str(relative.with_suffix(""))
        existing.add(identifier)
    return existing
