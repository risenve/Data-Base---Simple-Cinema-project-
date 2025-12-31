# Database Final Project

REST API application for managing events, correspondents and reportages.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic

## Quick Start

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start PostgreSQL (if not running)
# On macOS:
brew services start postgresql
# On Linux:
sudo service postgresql start

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
psql -U postgres -c "CREATE DATABASE reportage_db;"
psql -U postgres -d reportage_db -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# 5. Apply migrations
alembic upgrade head

# 6. Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. In another terminal, populate database
python scripts/fill_db.py