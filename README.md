# BrainAlpha

A Python CLI toolbox for automating WorldQuant Brain alpha research workflows. The project aims to turn repetitive
web actions—creating alphas, running backtests, and submitting qualified strategies—into a scriptable pipeline that can
also collaborate with LLMs.

## Vision & Scope
- Manage credentials and API access for WorldQuant Brain.
- Provide CLI commands for alpha CRUD, backtests, submissions, and data schema discovery.
- Integrate LLMs to propose or refine alpha expressions based on field metadata and prior performance.
- Enable end-to-end pipelines: generate → validate → backtest → qualify → submit.
- Keep the architecture cleanly layered (infra, services, CLI) so future Web/App clients can reuse the core services.

## Project Milestones
- **M1:** Project skeleton, configuration system, logging, and CLI scaffolding.
- **M2:** WorldQuant Brain API client with alpha CRUD and backtests.
- **M3:** LLM-driven alpha generation with validation.
- **M4:** Automated qualify-and-submit pipeline driven by config files.
- **M5:** Documentation and stable service interfaces for downstream clients.

## Getting Started

### Installation (editable)
```bash
pip install --editable .
```

### Commands
- `brainalpha version` — show installed version.
- `brainalpha config init` — write credentials and defaults to `~/.brainalpha/config.yml`.
- `brainalpha config show` — view saved configuration (secrets are redacted).

## Configuration
Configuration is stored at `~/.brainalpha/config.yml` by default. The file captures:

- `api_key`: WorldQuant Brain API key (kept private; file permissions set to `600`).
- `base_url`: API base URL (defaults to production endpoint).
- `storage_path`: Local directory for caching artifacts and backtests.

You can override the config path by instantiating `ConfigManager` with a custom path.

## Development Notes
- Packaging uses [`hatchling`](https://hatch.pypa.io/latest/).
- CLI built on [`typer`](https://typer.tiangolo.com/) and [`rich`](https://rich.readthedocs.io/).
- HTTP interactions use [`httpx`](https://www.python-httpx.org/) with a lightweight retry helper.

## Roadmap
See `configs/sample.yml` for an example of future pipeline configuration. Upcoming work will flesh out API services,
backtest orchestration, qualification rules, and LLM prompt templates.
