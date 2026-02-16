"""
Generator: sends file content to an AI model and gets back
markdown documentation suitable for OtterWiki pages.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a technical writer creating internal documentation for an OtterWiki.

You will receive the full source code of a file. Read it carefully and produce a clear,
well-structured markdown documentation page.

## Output format

Use this structure (adjust sections as needed based on the code):

1. **Title** (H1) - A clear name for the endpoint/task.
2. **Overview** - 2-3 sentences explaining what this code does and why.
3. **Details** - The important specifics:
   - For APIs: HTTP method, URL, request/response shape, authentication.
   - For tasks/jobs: what it does step-by-step, inputs, outputs, scheduling.
4. **How it works** - A concise walkthrough of the logic.
5. **Notes** - Edge cases, dependencies, environment variables, or anything
   a developer should know. Use [TODO] for anything you can't determine.

## Rules
- Write in plain markdown (no wrapping code fences around the whole output).
- Be concise but thorough.
- If something is unclear from the code, make your best guess and mark it [TODO].
- Include relevant code snippets where helpful (short ones only).
- Keep it scannable - use bullet points and tables where appropriate."""


def generate_doc(file_info: dict, model: str | None = None) -> str:
    """
    Generate markdown documentation for a single file.

    Args:
        file_info: Dict with keys name, slug, path, content, subfolder.
        model: OpenAI model override.

    Returns:
        Markdown string.
    """
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Truncate very large files to stay within token limits
    content = file_info["content"]
    if len(content) > 15000:
        content = content[:15000] + "\n\n// ... file truncated for length ..."

    user_prompt = f"""File: {file_info['relative_path']}
Category: {file_info['subfolder']}

```
{content}
```

Write markdown documentation for this file."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=3000,
    )

    return response.choices[0].message.content.strip()
