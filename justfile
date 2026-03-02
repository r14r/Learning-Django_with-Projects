# justfile — Learning Django with Projects
# Run `just` (or `just --list`) to see all available commands.
# Each project's `final` step contains its own justfile with Django-specific commands.

default:
    @just --list

# ── Repository overview ───────────────────────────────────────────────────────

# List all beginner projects
list-beginner:
    @ls 10_beginner/

# List all advanced projects
list-advanced:
    @ls 20_advanced/

# List all expert projects
list-expert:
    @ls 30_expert/

# List every project across all levels
list-all:
    @echo "=== Beginner ===" && ls 10_beginner/ && echo "" \
    && echo "=== Advanced ===" && ls 20_advanced/ && echo "" \
    && echo "=== Expert ===" && ls 30_expert/

# ── Setup ─────────────────────────────────────────────────────────────────────

# Create a virtual environment and install uv
setup:
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install uv

# Install dependencies from a requirements.txt (run inside a project's src/)
install:
    uv pip install -r requirements.txt

# ── Working with a project ───────────────────────────────────────────────────
# To work on a project, navigate to its `steps/final/src/` directory, then use
# the project-level `justfile` commands:
#
#   cd 10_beginner/01_hello_django/steps/final/src
#   just setup       # create .venv and install deps
#   just migrate     # apply database migrations
#   just run         # start the dev server
#   just test        # run the test suite

