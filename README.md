# Data Governor

AI-assisted data governance tooling for understanding, organising, and safely managing files.

Data Governor is designed around one hard rule: AI never directly modifies files. Intelligence produces structured metadata and confidence signals; deterministic code turns reviewed proposals into auditable filesystem operations.

## V0.1 Scope

The first milestone is a safe end-to-end media governance demo:

- configurable filesystem roots
- asset catalogue backed by SQLite
- scanner for a disposable Jellyfin-style test library
- proposal workflow for media rename/move operations
- human review before execution
- safe executor with path validation, collision checks, audit history, and undo

Later phases add document governance, OCR/classification, first-class profiles, catalogue search, and a knowledge layer.

## Repository Layout

```text
backend/              FastAPI application
frontend/             UI placeholder for the review experience
tests/                Automated tests
scripts/              Development and fixture scripts
dev-data/             Disposable local fixture data, not committed
docs/                 Product plan, milestones, and future roadmap
static/               Brand and concept assets
```

## Local Development

Create the disposable media fixture library:

```bash
./scripts/reset-test-library.sh
```

Run the backend with Docker Compose:

```bash
sudo docker-compose up --build
```

Then check:

```bash
curl http://localhost:8000/health
```

The container only mounts `./dev-data/media` at `/data/test-media`, keeping development operations away from any real NAS paths.

## Safety Principles

- store relative paths against configured roots
- resolve all filesystem operations through allowed-root helpers
- keep execution disabled by default outside the local sandbox
- create proposals first, execute only reviewed operations
- record enough audit history to undo every accepted change
