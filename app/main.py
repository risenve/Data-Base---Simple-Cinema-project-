from fastapi import FastAPI, HTTPException
import psycopg2
import os
from dotenv import load_dotenv
from .schemas import Event, Correspondent, Reportage

load_dotenv()
app = FastAPI(title="Reportage API")

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )

# EVENTS
@app.get("/events")
def get_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "place": r[1], "city": r[2], "date": r[3],
             "duration": r[4], "danger": r[5], "type": r[6]} for r in rows]

@app.post("/events")
def create_event(event: Event):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO events (place, city, date, duration, danger, type) VALUES (%s,%s,%s,%s,%s,%s);",
            (event.place, event.city, event.date, event.duration, event.danger, event.type)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"status": "created"}

# CORRESPONDENTS
@app.get("/correspondents")
def get_correspondents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM correspondent;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "country": r[2], "city": r[3],
             "specification": r[4], "operator": r[5], "price": float(r[6])} for r in rows]

@app.post("/correspondents")
def create_correspondent(c: Correspondent):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO correspondent (name, country, city, specification, operator, price) VALUES (%s,%s,%s,%s,%s,%s);",
            (c.name, c.country, c.city, c.specification, c.operator, c.price)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"status": "created"}

# REPORTAGES
@app.get("/reportages")
def get_reportages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportage;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "date": r[1], "quality": r[2], "time": str(r[3]),
             "video": r[4], "event_id": r[5], "correspondent_id": r[6]} for r in rows]

@app.post("/reportages")
def create_reportage(r: Reportage):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO reportage (date, quality, time, video, event_id, correspondent_id) VALUES (%s,%s,%s,%s,%s,%s);",
            (r.date, r.quality, r.time, r.video, r.event_id, r.correspondent_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"status": "created"}