# Honyaku OtterWiki

Internal documentation wiki for Honyaku, powered by [OtterWiki](https://otterwiki.com). Includes scripts to auto-generate documentation by scanning the Xanoscript codebase and using an AI model to produce markdown.

## Architecture

```
honyaku-otterwiki/
├── docker-compose.yaml          # Runs OtterWiki (optional, for hosted wiki UI)
├── wiki-content/                # Markdown docs (committed to GitHub)
│   ├── Home.md                  # Wiki homepage
│   ├── apis/                    # API endpoint docs
│   ├── functions/               # Xanoscript function docs
│   ├── agents/                  # AI agent docs
│   ├── mcp_servers/             # MCP server docs
│   ├── middlewares/             # Middleware docs
│   ├── tables/                  # Database table docs
│   ├── tasks/                   # Scheduled task/job docs
│   └── shunyaku/               # Team-contributed pages (manual)
├── scripts/                     # Doc generation scripts (run locally)
│   ├── run.py                   # Main entry point
│   ├── scanner.py               # Reads files from Xano project
│   ├── generator.py             # Sends code to AI, gets markdown back
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variable template
│   └── .env                     # Your local config (git-ignored)
└── app-data/                    # OtterWiki runtime data (git-ignored, local only)
```

### How it works

1. **`wiki-content/`** is the source of truth for all documentation. It's committed to GitHub and readable there directly.
2. **`scripts/`** scan the Xanoscript project (`xano-scripts/honyakuOS`), compare against existing docs, and use OpenAI to generate markdown for anything new.
3. **OtterWiki** (optional) can be run in Docker if you want a browsable wiki UI. It reads from its own git repo at `app-data/repository/` which the scripts sync into.

### Workflow: local scripts → GitHub → (optional) hosted wiki

```
You run scripts locally          GitHub                    Forge (optional)
┌─────────────────────┐    ┌──────────────┐    ┌──────────────────────┐
│ 1. Scan Xano project│    │              │    │                      │
│ 2. Generate markdown │───>│ wiki-content/ │───>│ OtterWiki serves     │
│ 3. Commit & push     │    │ on GitHub    │    │ pages from git repo  │
└─────────────────────┘    └──────────────┘    └──────────────────────┘
```

- **Without Forge**: Docs are readable directly on GitHub as markdown files.
- **With Forge**: OtterWiki gives you a searchable wiki UI. See "Hosting on Forge" section below.

---

## Prerequisites

- **Python 3.10+** (for running the doc generation scripts)
- **An OpenAI API key** (for AI-generated documentation)
- **Git** (wiki content is version-controlled)
- **Docker** (only needed if running OtterWiki locally or on a server)

---

## 1. Setup Doc Generation Scripts

These scripts run on your local machine. They scan the Xanoscript project and generate wiki pages for anything new.

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
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

### Run

From the project root:

```bash
# Dry run — see what files need docs without generating anything
python scripts/run.py --target ../xano-scripts/honyakuOS --dry-run

# Generate docs for all new files
python scripts/run.py --target ../xano-scripts/honyakuOS

# Generate but skip git commit/push
python scripts/run.py --target ../xano-scripts/honyakuOS --no-git

# Only scan specific folders
python scripts/run.py --target ../xano-scripts/honyakuOS --folders apis tasks

# Skip syncing to local OtterWiki
python scripts/run.py --target ../xano-scripts/honyakuOS --no-sync
```

### What the script does

1. **Scans** the Xanoscript project folders: `apis/`, `functions/`, `agents/`, `mcp_servers/`, `middlewares/`, `tables/`, `tasks/`.
2. **Compares** against existing `.md` files in `wiki-content/`. Only files without a matching doc are flagged as new.
3. **Generates** markdown documentation for new files by sending the source code to OpenAI.
4. **Writes** the markdown to the matching folder in `wiki-content/`.
5. **Syncs** to local OtterWiki (if running) so pages appear immediately.
6. **Commits and pushes** to GitHub (unless `--no-git`).

### Idempotency

Running the script multiple times is safe. It only generates docs for files that don't already have a `.md` in `wiki-content/`. Existing docs are never overwritten.

To regenerate a doc: delete its `.md` file from `wiki-content/` and run again.

### Shunyaku pages

The `wiki-content/shunyaku/` folder is for manually written pages. The scripts never touch this folder. Anyone can add `.md` files here, commit, and push.

---

## 2. Hosting on Forge (Optional)

If you want a browsable wiki UI instead of just reading markdown on GitHub.

### Does it need a database?

**No.** OtterWiki uses SQLite (file-based) for user accounts. Wiki content is stored as markdown in a git repo. No MySQL or Postgres needed.

### Deploy steps

1. **Create a server on Forge** (or use an existing one). Minimal resources needed (~100MB RAM).

2. **Install Docker** on the server if not already present.

3. **Clone and start:**
   ```bash
   cd /home/forge
   git clone git@github.com:Dylaan94/honyaku-otterwiki.git
   cd honyaku-otterwiki
   docker compose up -d
   ```

4. **Set up Nginx reverse proxy** in Forge. Create a site (e.g. `wiki.honyaku.org`) with this config:

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

5. **Enable SSL** via Forge's Let's Encrypt.

6. **Register** the first account — it becomes the admin automatically.

### Syncing GitHub docs to OtterWiki on the server

After you push new docs to GitHub, SSH into the server and run:

```bash
cd /home/forge/honyaku-otterwiki
git pull
# Copy updated wiki-content into OtterWiki's repo
cp -r wiki-content/apis wiki-content/functions wiki-content/agents \
      wiki-content/mcp_servers wiki-content/middlewares wiki-content/tables \
      wiki-content/tasks wiki-content/shunyaku app-data/repository/
cp wiki-content/Home.md app-data/repository/home.md
cd app-data/repository
git add -A && git commit -m "sync from GitHub"
```

Or automate this with a Forge deployment script that runs on each push.

---

## Useful Commands

```bash
# Dry run (see what needs docs)
python scripts/run.py --target ../xano-scripts/honyakuOS --dry-run

# Generate all new docs
python scripts/run.py --target ../xano-scripts/honyakuOS

# Generate only API docs
python scripts/run.py --target ../xano-scripts/honyakuOS --folders apis

# Start local OtterWiki
docker compose up -d

# Stop local OtterWiki
docker compose down

# View OtterWiki logs
docker compose logs -f otterwiki
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8080 already in use | Change the port in `docker-compose.yaml` (e.g. `9090:80`) |
| OpenAI API errors | Check `OPENAI_API_KEY` in `scripts/.env` |
| No files found | Check `--target` path points to the Xanoscript project root |
| Docs not showing in OtterWiki | Run with `--no-sync` disabled, or manually copy to `app-data/repository/` |
| Git push fails | Check you have push access to the GitHub repo |
