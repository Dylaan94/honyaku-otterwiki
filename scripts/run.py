#!/usr/bin/env python3
"""
Scan a Xanoscript project, generate markdown documentation for any
files that don't already have a wiki page, and sync to OtterWiki.
Preserves subfolder structure from the source project.

Usage:
    python scripts/run.py --target /path/to/xano-project
    python scripts/run.py --target /path/to/xano-project --dry-run
    python scripts/run.py --target /path/to/xano-project --no-git
    python scripts/run.py --target /path/to/xano-project --folders apis tasks
    python scripts/run.py --target /path/to/xano-project --folders apis --filter docling llm
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

scripts_dir = Path(__file__).resolve().parent
project_root = scripts_dir.parent
load_dotenv(scripts_dir / ".env")

from scanner import scan_project, get_existing_docs, SCAN_FOLDERS
from generator import generate_doc


def write_doc(wiki_dir: Path, wiki_path: str, slug: str, content: str) -> Path:
    """Write a markdown file preserving subfolder structure."""
    folder = wiki_dir / wiki_path
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f"{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def sync_file_to_otterwiki(filepath: Path, wiki_path: str):
    """Copy a single doc file into OtterWiki's repo immediately."""
    otterwiki_repo = project_root / "app-data" / "repository"
    if not otterwiki_repo.exists():
        return

    dst_dir = otterwiki_repo / wiki_path
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(filepath, dst_dir / filepath.name)


def sync_home_to_otterwiki():
    """Sync Home.md to OtterWiki."""
    otterwiki_repo = project_root / "app-data" / "repository"
    if not otterwiki_repo.exists():
        return
    home = project_root / "wiki-content" / "Home.md"
    if home.exists():
        shutil.copy2(home, otterwiki_repo / "home.md")


def commit_otterwiki(message: str = "docs: sync from wiki-content"):
    """Commit all pending changes in OtterWiki's repo."""
    otterwiki_repo = project_root / "app-data" / "repository"
    if not otterwiki_repo.exists():
        print("  [skip] app-data/repository/ not found (OtterWiki not running locally).")
        return

    try:
        import git
        repo = git.Repo(otterwiki_repo)
        repo.git.add(A=True)
        if repo.is_dirty(index=True):
            repo.index.commit(message)
            print("  Synced to OtterWiki.")
        else:
            print("  OtterWiki already up to date.")
    except Exception as e:
        print(f"  OtterWiki sync error: {e}")


def git_commit_and_push(message: str):
    """Stage, commit, and push changes in the main project repo."""
    try:
        import git
        repo = git.Repo(project_root)
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
    parser = argparse.ArgumentParser(description="Scan Xanoscript project and generate wiki docs.")
    parser.add_argument("--target", required=True, help="Path to the Xanoscript project root")
    parser.add_argument("--wiki-dir", default=None, help="Wiki content dir (default: ../wiki-content)")
    parser.add_argument("--dry-run", action="store_true", help="List what would be generated, don't do it")
    parser.add_argument("--no-git", action="store_true", help="Skip git commit/push")
    parser.add_argument("--no-sync", action="store_true", help="Skip syncing to local OtterWiki")
    parser.add_argument("--folders", nargs="*", default=None, help="Only scan these folders (e.g. apis tasks functions)")
    parser.add_argument("--filter", nargs="*", default=None, help="Only include files whose path contains one of these strings (e.g. docling llm phrase_endpoints)")
    parser.add_argument("--model", default=None, help="OpenAI model override")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    if not target_dir.is_dir():
        print(f"ERROR: Target directory not found: {target_dir}")
        sys.exit(1)

    wiki_dir = Path(args.wiki_dir).resolve() if args.wiki_dir else (project_root / "wiki-content").resolve()
    wiki_dir.mkdir(parents=True, exist_ok=True)

    model = args.model or os.getenv("OPENAI_MODEL", "gpt-4o")

    print(f"Scanning  : {target_dir}")
    print(f"Wiki dir  : {wiki_dir}")
    print(f"Model     : {model}")
    if args.folders:
        print(f"Folders   : {', '.join(args.folders)}")
    if args.filter:
        print(f"Filter    : {', '.join(args.filter)}")
    print()

    # Scan the project
    files = scan_project(str(target_dir), folders=args.folders)

    # Apply path filter if provided
    if args.filter:
        files = [f for f in files if any(flt in f["relative_path"] for flt in args.filter)]

    print(f"Found {len(files)} file(s) in project.")

    # Check what already has docs
    existing = get_existing_docs(str(wiki_dir))
    print(f"Existing docs: {len(existing)}")
    print()

    # Filter to files without docs — match on wiki_path/slug
    new_files = []
    for f in files:
        doc_id = f"{f['wiki_path']}/{f['slug']}"
        if doc_id not in existing:
            new_files.append(f)

    if not new_files:
        print("Everything is up to date. No new docs needed.")
        return

    print(f"{len(new_files)} file(s) need documentation:")
    for f in new_files:
        print(f"  [{f['wiki_path']}] {f['name']} -> {f['wiki_path']}/{f['slug']}.md")
    print()

    if args.dry_run:
        print("Dry run complete.")
        return

    # Generate docs — each file is synced to OtterWiki immediately
    generated = []
    for i, f in enumerate(new_files, 1):
        print(f"[{i}/{len(new_files)}] Generating: {f['relative_path']}...")
        try:
            markdown = generate_doc(f, model=model)
            path = write_doc(wiki_dir, f["wiki_path"], f["slug"], markdown)
            generated.append(path)
            print(f"  -> wiki-content/{f['wiki_path']}/{f['slug']}.md")

            # Immediately copy to OtterWiki so it's available right away
            if not args.no_sync:
                sync_file_to_otterwiki(path, f["wiki_path"])
        except Exception as e:
            print(f"  ERROR: {e}")
    print()

    # Commit all synced files to OtterWiki's repo in one go
    if generated and not args.no_sync:
        print("=== Syncing to OtterWiki ===")
        sync_home_to_otterwiki()
        commit_otterwiki(f"docs: add {len(generated)} page(s)")

    # Git commit/push
    if generated and not args.no_git:
        print("=== Git ===")
        msg = f"docs: auto-generate {len(generated)} new wiki page(s)"
        git_commit_and_push(msg)

    print(f"\nDone. Generated {len(generated)} doc(s).")


if __name__ == "__main__":
    main()
