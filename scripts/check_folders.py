#!/usr/bin/env python3
"""
Check the Xanoscript project for any new top-level folders that
aren't yet tracked by the wiki. Prompts to add them.

Usage:
    python scripts/check_folders.py --target ../xano-scripts/honyakuOS
"""

import argparse
import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent
project_root = scripts_dir.parent

# Folders we skip (not relevant for documentation)
IGNORE_FOLDERS = {
    ".git",
    ".github",
    ".cursor",
    ".xano",
    "docs",
    "node_modules",
    "__pycache__",
}


def get_xano_folders(target_dir: Path) -> set[str]:
    """Get all top-level folders in the Xano project."""
    return {
        f.name
        for f in sorted(target_dir.iterdir())
        if f.is_dir() and not f.name.startswith(".") and f.name not in IGNORE_FOLDERS
    }


def get_wiki_folders() -> set[str]:
    """Get existing wiki-content subfolders."""
    wiki_dir = project_root / "wiki-content"
    return {
        f.name
        for f in sorted(wiki_dir.iterdir())
        if f.is_dir()
    }


def get_scanner_folders() -> list[str]:
    """Read the current SCAN_FOLDERS from scanner.py."""
    from scanner import SCAN_FOLDERS
    return list(SCAN_FOLDERS)


def main():
    parser = argparse.ArgumentParser(description="Check for new folders in the Xano project.")
    parser.add_argument("--target", required=True, help="Path to the Xanoscript project root")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"ERROR: Directory not found: {target_dir}")
        sys.exit(1)

    xano_folders = get_xano_folders(target_dir)
    wiki_folders = get_wiki_folders()
    scanner_folders = set(get_scanner_folders())

    # Manual-only folders that exist in wiki but not in xano
    manual_folders = {"shunyaku"}

    tracked = scanner_folders | manual_folders
    new_folders = xano_folders - tracked

    print(f"Xano project    : {target_dir}")
    print(f"Xano folders    : {', '.join(sorted(xano_folders))}")
    print(f"Tracked in wiki : {', '.join(sorted(tracked))}")
    print()

    if not new_folders:
        print("No new folders found. Everything is tracked.")
        return

    print(f"New folders found ({len(new_folders)}):")
    for folder in sorted(new_folders):
        # Count files in the folder
        file_count = sum(1 for f in (target_dir / folder).rglob("*") if f.is_file() and not f.name.startswith("."))
        print(f"  {folder}/ ({file_count} file(s))")

    print()
    print("Would you like to add any of these to the wiki?")
    print("Enter folder names separated by spaces, or 'all' to add all, or 'none' to skip:")
    print()

    answer = input("> ").strip().lower()

    if answer == "none" or answer == "":
        print("Skipped.")
        return

    if answer == "all":
        to_add = sorted(new_folders)
    else:
        to_add = [f.strip() for f in answer.split() if f.strip() in new_folders]
        invalid = [f.strip() for f in answer.split() if f.strip() not in new_folders]
        if invalid:
            print(f"  [warn] Skipping unknown folders: {', '.join(invalid)}")

    if not to_add:
        print("Nothing to add.")
        return

    # Create wiki-content folders
    wiki_dir = project_root / "wiki-content"
    for folder in to_add:
        folder_path = wiki_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: wiki-content/{folder}/")

    # Update scanner.py SCAN_FOLDERS
    scanner_path = scripts_dir / "scanner.py"
    scanner_content = scanner_path.read_text(encoding="utf-8")

    new_scan_list = sorted(scanner_folders | set(to_add))
    new_list_str = "SCAN_FOLDERS = [\n"
    for folder in new_scan_list:
        new_list_str += f'    "{folder}",\n'
    new_list_str += "]"

    # Replace the existing SCAN_FOLDERS block
    import re
    scanner_content = re.sub(
        r"SCAN_FOLDERS = \[.*?\]",
        new_list_str,
        scanner_content,
        flags=re.DOTALL,
    )
    scanner_path.write_text(scanner_content, encoding="utf-8")
    print(f"\n  Updated scanner.py SCAN_FOLDERS: {', '.join(new_scan_list)}")

    # Update Home.md
    home_path = wiki_dir / "Home.md"
    if home_path.exists():
        home_content = home_path.read_text(encoding="utf-8")
        for folder in to_add:
            label = folder.replace("_", " ").title()
            link_line = f"- [{label}]({folder}/) - {label} documentation"
            if folder not in home_content:
                # Insert before the shunyaku line or at end of sections
                if "shunyaku" in home_content:
                    home_content = home_content.replace(
                        "- [Shunyaku]",
                        f"{link_line}\n- [Shunyaku]",
                    )
                else:
                    home_content = home_content.rstrip() + f"\n{link_line}\n"
        home_path.write_text(home_content, encoding="utf-8")
        print("  Updated Home.md with new sections.")

    print(f"\nDone. Added {len(to_add)} folder(s). You can now run:")
    print(f"  python scripts/run.py --target {args.target} --folders {' '.join(to_add)} --dry-run")


if __name__ == "__main__":
    main()
