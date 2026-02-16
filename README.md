# Honyaku OtterWiki

Internal documentation wiki for Honyaku APIs and tasks, powered by [OtterWiki](https://otterwiki.com). Includes scripts to auto-generate documentation by scanning a code directory and using an AI model to produce markdown.

## Architecture

```
honyaku-otterwiki/
├── docker-compose.yaml          # Runs OtterWiki (for Laravel Forge)
├── wiki-content/                # Markdown docs (committed to git)
│   ├── Home.md                  # Wiki homepage
│   ├── apis/                    # API endpoint documentation
│   │   └── *.md
│   └── tasks/                   # Task/job documentation
│       └── *.md
├── scripts/                     # Doc generation scripts (run locally)
│   ├── run.py                   # Main entry point
│   ├── scanner.py               # Reads files from target directory
│   ├── generator.py             # Sends code to AI, gets markdown back
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variable template
│   └── .env                     # Your local config (git-ignored)
└── app-data/                    # OtterWiki runtime data (git-ignored)
```

### How it works

1. **OtterWiki** runs in Docker and serves the wiki UI. It stores pages as markdown in a git repo. No external database needed — it uses SQLite internally for user accounts.
2. **`wiki-content/`** is where all the markdown documentation lives. This is committed to GitHub.
3. **`scripts/`** scan a target code directory, compare against existing docs in `wiki-content/`, and use OpenAI to generate markdown for anything new.

---

## Prerequisites

- **Docker** and **Docker Compose** (for running OtterWiki)
- **Python 3.10+** (for running the doc generation scripts locally)
- **An OpenAI API key** (for AI-generated documentation)
- **Git** (the wiki content is version-controlled)

---

## 1. Setup OtterWiki on Laravel Forge

### Does it need a database?

**No.** OtterWiki uses an embedded SQLite database for user accounts and settings. The actual wiki content is stored as markdown files in a git repository. There is no need to provision MySQL, Postgres, or any external database.

### Deploy steps

1. **Create a new server on Forge** (or use an existing one). A small server is fine — OtterWiki needs minimal CPU/RAM (~100MB).

2. **SSH into the server** and clone this repo:
   ```bash
   cd /home/forge
   git clone https://github.com/YOUR_ORG/honyaku-otterwiki.git
   cd honyaku-otterwiki
   ```

3. **Start OtterWiki with Docker Compose:**
   ```bash
   docker compose up -d
   ```
   This starts OtterWiki on port `8080`.

4. **Set up a reverse proxy in Forge.** Create a new site (e.g. `wiki.yourdomain.com`) and configure Nginx to proxy to port 8080. Add this to the Nginx config for the site:

   ```nginx
   location / {
       proxy_set_header Host $http_host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Host $http_host;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_pass http://127.0.0.1:8080;
       client_max_body_size 64M;
   }
   ```

5. **Enable SSL** via Forge's Let's Encrypt integration.

6. **Open the wiki** at `https://wiki.yourdomain.com`. Register the first account — this becomes the admin account (no email confirmation needed for the first user).

7. **Configure the wiki** in the admin settings (site name, description, permissions, etc.).

### Environment variables (optional)

You can customise OtterWiki by adding environment variables to `docker-compose.yaml`:

```yaml
environment:
  SITE_NAME: "Honyaku Wiki"
  SITE_DESCRIPTION: "API & Task Documentation"
```

See [OtterWiki Configuration](https://otterwiki.com/Configuration) for all options.

### Keeping it running

Forge can manage the Docker process as a daemon. Or simply rely on `restart: unless-stopped` in the compose file — Docker will restart it after server reboots.

---

## 2. Setup Doc Generation Scripts (Local)

These scripts run on your local machine to scan a code directory and generate wiki pages.

### Install

```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

Edit `scripts/.env`:

```env
# Required: your OpenAI API key
OPENAI_API_KEY=sk-your-key-here

# Optional: change the model (default: gpt-4o)
OPENAI_MODEL=gpt-4o
```

### Run

From the project root:

```bash
# Scan a directory and generate docs for new files
python scripts/run.py --target /path/to/your/code/directory

# Dry run — see what would be generated without doing it
python scripts/run.py --target /path/to/your/code/directory --dry-run

# Generate docs but skip git commit/push
python scripts/run.py --target /path/to/your/code/directory --no-git

# Only scan files with specific extensions
python scripts/run.py --target /path/to/your/code/directory --extensions .query .task
```

### What the script does

1. **Scans** every file in `--target` directory (recursively).
2. **Classifies** each file as an API or task based on folder names and content.
3. **Compares** against existing `.md` files in `wiki-content/apis/` and `wiki-content/tasks/`.
4. **Generates** markdown documentation for any new files by sending the source code to an OpenAI model.
5. **Writes** the markdown to `wiki-content/apis/` or `wiki-content/tasks/`.
6. **Commits and pushes** the new docs to git (unless `--no-git` is passed).

### File classification

The script determines whether a file is an API or task by:
- **Folder name**: if the file is inside a folder containing "api", "endpoint", or "route" it goes to `apis/`. If it contains "task", "command", or "job" it goes to `tasks/`.
- **Content**: if the first line contains `query` with `verb=` it's classified as an API.
- **Default**: files that can't be classified go to `apis/`.

### Idempotency

The script only generates docs for files that don't already have a corresponding `.md` file in `wiki-content/`. It matches by filename (slug). So running it multiple times is safe — it won't regenerate existing docs.

To regenerate a doc, delete the `.md` file from `wiki-content/` and run again.

---

## 3. Uploading to OtterWiki

The generated markdown in `wiki-content/` is committed to this git repo. To get it into the running OtterWiki instance:

**Option A: Manual upload** — Copy/paste the markdown content into the OtterWiki web editor.

**Option B: Git sync** — OtterWiki's data store is a git repo at `app-data/repository/`. You could set up a script or webhook to copy `wiki-content/` files into that repo. [TODO: automate this if needed]

---

## Useful Commands

```bash
# Start OtterWiki
docker compose up -d

# Stop OtterWiki
docker compose down

# View OtterWiki logs
docker compose logs -f otterwiki

# Restart after config changes
docker compose restart

# Generate docs (from project root, with venv activated)
python scripts/run.py --target /path/to/code --dry-run
python scripts/run.py --target /path/to/code
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8080 already in use | Change the port mapping in `docker-compose.yaml` (e.g. `9090:80`) |
| OpenAI API errors | Check your `OPENAI_API_KEY` in `scripts/.env` |
| No files found when scanning | Check that `--target` points to the right directory and `--extensions` matches your file types |
| Git push fails | Make sure you have push access to the remote and the repo is initialised |
# honyaku-otterwiki
