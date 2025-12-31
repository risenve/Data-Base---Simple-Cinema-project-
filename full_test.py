
import sys
sys.path.insert(0, '.')

print("=== Full Diagnostic Test ===")
try:
    from app.database import Base, engine, SessionLocal
    print("✅ Database imports OK")
except Exception as e:
    print(f"❌ Database import error: {e}")

try:
    from app.models import Event
    print("✅ Event model import OK")
    
    # Check columns
    print(f"Event columns: {[c.name for c in Event.__table__.columns]}")
except Exception as e:
    print(f"❌ Model error: {e}")
# 3. Test schema
try:
    from app.schemas import EventResponse
    print("✅ EventResponse schema import OK")
except Exception as e:
    print(f"❌ Schema error: {e}")

# 4. Test database connection
try:
    from sqlalchemy import text
    db = SessionLocal()
    result = db.execute(text("SELECT 1"))
    print("✅ Database connection OK")
    db.close()
except Exception as e:
    print(f"❌ Database connection error: {e}")

# 5. Test actual query
try:
    db = SessionLocal()
    # Try simplest query
    result = db.execute(text("SELECT id, place FROM events LIMIT 1"))
    rows = result.fetchall()
    print(f"✅ Simple query OK. Found {len(rows)} rows")
    db.close()
except Exception as e:
    print(f"❌ Query error: {e}")

# 6. Test SQLAlchemy query
try:
    db = SessionLocal()
    # Query with SQLAlchemy ORM
    events = db.query(Event).limit(1).all()
    print(f"✅ SQLAlchemy query OK. Found {len(events)} events")
    db.close()
except Exception as e:
    print(f"❌ SQLAlchemy query error: {e}")
    import traceback
    traceback.print_exc()

print("=== End Diagnostic ===")
