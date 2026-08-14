# deploy

Fork the repo, and it runs itself: `.github/workflows/triage.yml` scans daily, runs the tests
first, and commits refreshed data and reports back to the default branch.

To point it at another project, change the repo and workflow name in the scan step. First run on
a fresh project: expect the ~1000-result listing cap - backfill older history with
`scan --created A..B` windows.

The model stage is optional and off by default. To enable it anywhere:

    FLAKETRIAGE_MODEL_URL   openai-compatible endpoint (default http://localhost:11434/v1, ollama)
    FLAKETRIAGE_MODEL       model name (default qwen2.5:3b)
    FLAKETRIAGE_MODEL_KEY   only for hosted endpoints

Local setup: install ollama, `ollama pull qwen2.5:3b`, done. Everything else is python3 plus a
logged-in `gh`. There is no service, no database, no queue - state is one JSON file.
