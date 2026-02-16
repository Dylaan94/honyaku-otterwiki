#!/usr/bin/env python3
"""
Scan a directory for code files, generate markdown documentation
for any files that don't already have a wiki page, and optionally
commit + push to git.

Usage:
    python scripts/run.py --target /path/to/code/directory
    python scripts/run.py --target /path/to/code --dry-run
    python scripts/run.py --target /path/to/code --no-git
    python scripts/run.py --target /path/to/code --extensions .query .task
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

scripts_dir = Path(__file__).resolve().parent
load_dotenv(scripts_dir / ".env")

from scanner import scan_directory, get_existing_docs
from generator import generate_doc


def write_doc(wiki_dir: Path, subfolder: str, slug: str, content: str) -> Path:
    """Write a markdown file to the wiki content directory."""
    folder = wiki_dir / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f"{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def sync_to_otterwiki(wiki_dir: Path, project_root: Path):
    """Copy wiki-content/ into app-data/repository/ and commit so OtterWiki serves the new pages."""
    import shutil

    otterwiki_repo = project_root / "app-data" / "repository"
    if not otterwiki_repo.exists():
        print("  [skip] app-data/repository/ not found (OtterWiki not running locally).")
        return

    for subfolder in ["apis", "tasks"]:
        src = wiki_dir / subfolder
        dst = otterwiki_repo / subfolder
        if src.exists():
            dst.mkdir(parents=True, exist_ok=True)
            for md_file in src.glob("*.md"):
                shutil.copy2(md_file, dst / md_file.name)

    # Also sync Home.md
    home = wiki_dir / "Home.md"
    if home.exists():
        shutil.copy2(home, otterwiki_repo / "home.md")

    # Commit inside the OtterWiki repo
    try:
        import git
        repo = git.Repo(otterwiki_repo)
        repo.git.add(A=True)
        if repo.is_dirty(index=True):
            repo.index.commit("docs: sync from wiki-content")
            print("  Synced to OtterWiki (app-data/repository/).")
        else:
            print("  OtterWiki repo already up to date.")
    except Exception as e:
        print(f"  OtterWiki sync error: {e}")


def git_commit_and_push(repo_dir: Path, message: str):
    """Stage, commit, and push changes in the main project repo."""
    try:
        import git
        repo = git.Repo(repo_dir, search_parent_directories=True)
        repo.git.add(A=True)
        if repo.is_dirty(index=True):
            repo.index.commit(message)
            print(f"  Committed: {message}")
            if repo.remotes:
                repo.remotes.origin.push()
                print("  Pushed to remote.")
            else:
                print("  No remote found, skipping push.")
        else:
            print("  Nothing to commit.")
    except Exception as e:
        print(f"  Git error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Scan code and generate wiki docs.")
    parser.add_argument("--target", required=True, help="Directory to scan for code files")
    parser.add_argument("--wiki-dir", default=None, help="Wiki content dir (default: ../wiki-content)")
    parser.add_argument("--dry-run", action="store_true", help="List new files without generating docs")
    parser.add_argument("--no-git", action="store_true", help="Skip git commit/push")
    parser.add_argument("--extensions", nargs="*", default=None, help="File extensions to include (e.g. .query .task)")
    parser.add_argument("--model", default=None, help="OpenAI model override")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"ERROR: Target directory not found: {target_dir}")
        sys.exit(1)

    wiki_dir = Path(args.wiki_dir).resolve() if args.wiki_dir else (scripts_dir.parent / "wiki-content").resolve()
    wiki_dir.mkdir(parents=True, exist_ok=True)

    model = args.model or os.getenv("OPENAI_MODEL", "gpt-4o")

    print(f"Scanning  : {target_dir}")
    print(f"Wiki dir  : {wiki_dir}")
    print(f"Model     : {model}")
    print()

    # Scan the target directory
    files = scan_directory(str(target_dir), extensions=args.extensions)
    print(f"Found {len(files)} file(s) in target directory.")

    # Check existing docs
    existing = get_existing_docs(str(wiki_dir))
    print(f"Existing docs: {sum(len(v) for v in existing.values())} total")
    print()

    # Filter to new files only
    new_files = []
    for f in files:
        if f["slug"] not in existing.get(f["subfolder"], set()):
            new_files.append(f)

    if not new_files:
        print("Everything is up to date. No new docs needed.")
        return

    print(f"{len(new_files)} new file(s) need documentation:")
    for f in new_files:
        print(f"  [{f['subfolder']}] {f['relative_path']} -> {f['slug']}.md")
    print()

    if args.dry_run:
        print("Dry run complete.")
        return

    # Generate docs
    generated = []
    for i, f in enumerate(new_files, 1):
        print(f"[{i}/{len(new_files)}] Generating: {f['name']}...")
        try:
            markdown = generate_doc(f, model=model)
            path = write_doc(wiki_dir, f["subfolder"], f["slug"], markdown)
            generated.append(path)
            print(f"  -> {path}")
        except Exception as e:
            print(f"  ERROR: {e}")
    print()

    # Sync to local OtterWiki instance (if running)
    if generated:
        print("=== Syncing to OtterWiki ===")
        sync_to_otterwiki(wiki_dir, scripts_dir.parent)

    # Git commit/push the project repo
    if generated and not args.no_git:
        print("=== Git ===")
        msg = f"docs: auto-generate {len(generated)} new wiki page(s)"
        git_commit_and_push(wiki_dir, msg)

    print(f"\nDone. Generated {len(generated)} doc(s).")


if __name__ == "__main__":
    main()
