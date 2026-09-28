Here’s the V0.1 implementation sequence I’d use. The main goal is to get to a safe end-to-end demo as early as possible, then add intelligence only where it’s needed.
Milestone 0 — Repo and runtime
Start with the smallest deployable skeleton.
data-governor/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── scanner/
│       ├── catalogue/
│       ├── profiles/
│       ├── proposals/
│       ├── executor/
│       └── intelligence/
├── frontend/
├── tests/
├── docker-compose.yml
├── Dockerfile
└── README.md

Initial stack:
Backend     FastAPI
Database    SQLite
ORM         SQLAlchemy / SQLModel
Frontend    simple React/Vite or HTMX
Runtime     Docker Compose
Filesystem pathlib / os

For V0.1, I’d lean toward FastAPI + SQLModel + HTMX unless you specifically want to build a richer React application. HTMX gets us to a functional NAS appliance-style interface quickly.
Success condition:
docker compose up


make a sandbox/test library part of the development setup from day one. That lets us exercise scanning, proposals, execution, collisions, failures, and undo without ever touching the real NAS.
For example:
data-governor/
├── dev-data/
│   └── media/
│       ├── incoming/
│       │   ├── Alien.1979.1080p.BluRay.mkv
│       │   ├── The.Matrix.1999.REMUX.mkv
│       │   ├── Dune.1984.1080p.mkv
│       │   ├── Dune.2021.2160p.mkv
│       │   ├── Severance.S01E01.2160p.mkv
│       │   ├── Severance.S01E02.2160p.mkv
│       │   └── something-weird.mkv
│       │
│       └── existing/
│           └── Movies/
│               └── Alien (1979)/
│                   └── Alien (1979).mkv

They don't need to be real video files initially. Empty files created with touch are enough to test most of the system:
touch "Alien.1979.1080p.BluRay.mkv"

Then in development configuration:
roots:
  - id: test-media
    name: Test Media
    path: /data/test-media
    writable: true

execution:
  enabled: true

Docker only gets access to that test directory:
Host                          Container

./dev-data/media     →        /data/test-media

So even a catastrophic bug in the executor cannot access the real NAS, because it isn't mounted into the container.
I'd actually take this one step further and create a repeatable fixture generator:
./scripts/reset-test-library.sh

Every time we run it, it destroys and recreates the sandbox:
Test Media
├── 01-clean/
│   └── Alien (1979)/
│       └── Alien (1979).mkv
│
├── 02-needs-renaming/
│   ├── alien1979.mkv
│   ├── The.Matrix.1999.REMUX.mkv
│   └── Dune.2021.2160p.mkv
│
├── 03-tv/
│   ├── Severance.S01E01.mkv
│   └── Severance.S01E02.mkv
│
├── 04-ambiguous/
│   ├── alien.mkv
│   └── dune.mkv
│
├── 05-collisions/
│   └── Alien.1979.mkv
│
├── 06-weird/
│   ├── movie final FINAL.mkv
│   ├── Some.Movie.[1080p].[x265].mkv
│   └── badly_named_file.mkv
│
└── 07-ignore/
    ├── poster.jpg
    ├── notes.txt
    └── .hidden

That becomes more than sample data: it becomes our acceptance-test dataset.
For instance, we can define expected behaviour:
Fixture	Expected
Already correct	No proposal
alien1979.mkv	Rename/move proposal
Severance.S01E01.mkv	TV proposal
dune.mkv	Low-confidence/review
Existing target	Collision/block
Unsupported .txt	Ignore
Hidden file	Ignore


Then after execution we can automatically verify the resulting directory tree against an expected tree. After Undo, we verify that it exactly matches the original tree again.
I’d therefore add a small Milestone 0.5 — Test Harness before we even build the real scanner: fixture generator, disposable test root, known expected outcomes, reset script, and a hard rule that early development runs against test data only.
Later, when we start V0.2 documents, we do exactly the same thing with dev-data/documents/ containing synthetic/sample PDFs representing bills, invoices, insurance letters, badly scanned documents, ambiguous documents, etc. That gives us a safe regression suite for every governance profile we add.


Milestone 1 — Configuration and filesystem boundaries
Before scanning anything, establish the safety perimeter.
Configuration could look like:
roots:
  - id: media
    path: /data/media
    writable: false

database:
  path: /config/governor.db

execution:
  enabled: false

The application should internally resolve every path against an allowed root.
Core helper:
resolve_asset_path(root_id, relative_path)


rather than letting arbitrary code manipulate:
/some/random/path

This becomes one of the most important safety rules in the application.
Deliverables
- Config loader
- Allowed-root model
- Path normalisation
- Read-only mode
- Validation preventing escape from configured roots
- Startup check for mounted folders
Milestone 2 — Database schema
Build the database before the scanner so the scanner has somewhere durable to put its observations.
I’d start with six core tables.
roots
id
name
path
writable
created_at

assets
id UUID
root_id
relative_path
original_relative_path
filename
extension
mime_type
size_bytes
mtime
fingerprint
first_seen_at
last_seen_at
status

Important point:
relative_path

should be stored instead of relying entirely on absolute filesystem paths.
That makes deployments less brittle.
scans
id
root_id
profile_id
status
started_at
completed_at
files_seen
files_new
files_changed
proposals_created

proposals
id
scan_id
asset_id
operation
source_relative_path
target_relative_path
confidence
reason
status
created_at
reviewed_at

execution_batches
id
scan_id
started_at
completed_at
status

execution_operations
id
batch_id
proposal_id
operation
source_relative_path
target_relative_path
status
executed_at
error

Later, metadata can either become JSON attached to an asset or separate typed tables.
For V0.1, JSON is probably enough:
assets.metadata_json

Milestone 3 — Scanner
Now build a scanner with zero AI and zero renaming.
Input:
root = /data/media

Output:
Scan #1

842 files discovered
842 assets catalogued
0 changes made

The scanner should:
walk directories
↓
ignore excluded paths
↓
identify files
↓
collect stat information
↓
calculate fingerprint
↓
match existing asset
↓
insert/update catalogue

For fingerprinting, I would not SHA-256 an entire 80 GB Blu-ray rip on every scan.
Start with something like:
file size
+
first 1 MB hash
+
last 1 MB hash

and call it a fingerprint, rather than pretending it is a cryptographic identity.
Full hashing can be optional later.
First API
POST /api/scans
GET  /api/scans
GET  /api/scans/{id}

Example:
{
  "root_id": "media",
  "profile_id": "jellyfin"
}

Milestone 4 — Profile contract
Before Jellyfin logic, define the interface that Jellyfin must conform to.
Something along the lines of:
class GovernanceProfile:    id: str    name: str    def matches(self, asset) -> bool:        ...    def analyse(self, asset) -> AnalysisResult:        ...    def target(self, asset, metadata) -> Target:        ...    def validate(self, proposal) -> ValidationResult:        ...


Core types:
class AnalysisResult:    metadata: dict    confidence: float    evidence: list[str]    warnings: list[str]


and:
class Target:    relative_path: str


Crucially:
Profile → proposed target

NOT

Profile → filesystem operation

That distinction will pay off later.
Milestone 5 — Jellyfin deterministic parser
Now implement the first actual profile.
Start with easy cases.
Movie
Alien.1979.1080p.BluRay.mkv

becomes:
{
  "type": "movie",
  "title": "Alien",
  "year": 1979
}

Target:
Movies/Alien (1979)/Alien (1979).mkv

TV
Severance.S01E03.2160p.mkv

becomes:
{
  "type": "episode",
  "series": "Severance",
  "season": 1,
  "episode": 3
}

Target:
TV Shows/
  Severance/
    Season 01/
      Severance S01E03.mkv

Initially support a deliberately small set of patterns:
Title.Year.ext
Title (Year).ext
Series.S01E02.ext
Series.S01E02.Title.ext

Ignore clever edge cases initially.
Milestone 6 — Proposal generation
At this point we can create the first useful workflow.
Asset
 ↓
Profile match
 ↓
Analyse
 ↓
Generate target
 ↓
Compare target to current path
 ↓
Proposal

If:
current == target

no proposal is created.
If different:
proposal.status = pending

Example:
{
  "asset_id": "abc",
  "source": "incoming/alien1979.mkv",
  "target": "Movies/Alien (1979)/Alien (1979).mkv",
  "confidence": 0.96,
  "reason": "Parsed title and year from filename"
}

Still no filesystem changes.
Milestone 7 — Review UI
This is the first point where the project starts feeling like the product.
Main pages:
/
    dashboard

/scans
    scan history

/scans/{id}
    proposals

/assets/{id}
    asset detail

The important screen is:
Scan #7

[✓] Alien                              96%
    incoming/alien1979.mkv

    →
    
    Movies/Alien (1979)/Alien (1979).mkv

    Parsed:
    title: Alien
    year: 1979

    [Accept] [Reject] [Edit]

Support:
- Accept
- Reject
- Edit target
- Multi-select
- Approve selected
No executor yet.
Milestone 8 — Dry-run executor
Build the execution system but have it only simulate.
Approved proposal
 ↓
Pre-flight validator
 ↓
Dry-run result

Possible output:
READY
source exists
destination available
root valid
no symlink escape
filesystem writable

or:
BLOCKED
destination already exists

Add:
POST /api/proposals/{id}/validate

and:
POST /api/scans/{id}/dry-run

This gives us a way to stress the safety code before letting anything actually move.
Milestone 9 — Real executor
Only after dry-run is working reliably.
Execution process:
load approved proposal
↓
revalidate source
↓
verify asset fingerprint
↓
validate destination
↓
create required directories
↓
move file
↓
verify destination exists
↓
update asset path
↓
write audit entry

If any step fails:
proposal → failed
operation → failed

but don't attempt clever automatic recovery yet.
V0.1 execution operations:
mkdir
rename
move

No:
delete
overwrite
merge
replace

Milestone 10 — Undo
Once files can move, undo must immediately follow.
For every operation:
A → B

store:
inverse = B → A

Before undo:
Does B still exist?
Is it still the same asset?
Is A free?

If yes:
B → A

If not:
undo blocked

Do not force it.
Milestone 11 — External metadata
Only now would I bring in TMDB or another provider.
Reason:
The full architecture should already function without it.
Create:
class MetadataProvider:    def search_movie(...)    def search_series(...)


Then:
Filename parser
      ↓
title/year candidate
      ↓
metadata provider
      ↓
canonical match

This is where:
alien1979.mkv

can turn into a highly confident match to:
Alien
1979
TMDB ID ...

and ambiguity can be exposed to the UI.
Milestone 12 — LLM fallback
The LLM comes last in V0.1.
For example:
Alien Final Directors Cut bluray.mkv

might fail deterministic parsing.
The pipeline becomes:
parser
 ↓
metadata lookup
 ↓
still ambiguous?
 ↓
LLM

The LLM receives limited context and must conform to a schema.
Example response:
{
  "media_type": "movie",
  "title": "Alien",
  "year": 1979,
  "confidence": 0.88,
  "evidence": [
    "Filename contains Alien",
    "Parent folder contains 1979"
  ]
}

The application — not the model — calculates:
Movies/Alien (1979)/Alien (1979).mkv

V0.1 API shape
By the end, something like:
GET  /api/roots
GET  /api/profiles

POST /api/scans
GET  /api/scans
GET  /api/scans/{id}

GET  /api/scans/{id}/proposals

GET   /api/assets/{id}

PATCH /api/proposals/{id}
POST  /api/proposals/{id}/approve
POST  /api/proposals/{id}/reject

POST /api/scans/{id}/dry-run
POST /api/scans/{id}/execute
POST /api/executions/{id}/undo

GET  /api/executions
GET  /api/executions/{id}

That's enough API surface for V0.1.
Explicitly postpone
This part matters just as much as the backlog.
For V0.1 I would not build:
OCR
Document profiles
Photo understanding
Semantic search
Vector database
Automatic approval
Automatic scheduled scans
Duplicate deletion
File deletion of any kind
User accounts
Multi-user permissions
Cloud deployment
Kubernetes
Model training
Complex workflow engine
Profile-builder UI
Plugin marketplace
Mobile application

Those are all plausible later features, but none help us prove the core system.
Recommended build order
So the actual sequence becomes:
01  Application skeleton
02  Filesystem safety/configuration
03  Database
04  Asset catalogue
05  Scanner
06  Profile interface
07  Jellyfin parser
08  Proposal engine
09  Review UI
10  Dry-run executor
11  Real executor
12  Audit + undo
13  Metadata provider
14  LLM fallback
15  Raspberry Pi deployment testing

And I'd define the V0.1 release gate very simply:
I can point Data Governor at a messy media folder on the NAS, scan it, review proposed Jellyfin-compatible changes in a browser, approve some of them, execute those changes safely, and undo them.

If we achieve that without the profile, scanner, proposal or executor layers knowing too much about one another, then we have the foundation we need for V0.2 documents.