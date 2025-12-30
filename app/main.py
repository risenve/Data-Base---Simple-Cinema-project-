from fastapi import FastAPI
import psycopg2
import os

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Reportage API")

# Database connection function
def get_connection():
    return psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )

# Adding an endpoint to fetch all events
@app.get("/events")
def get_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM events;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "place": row[1],
            "city": row[2],
            "date": row[3],
            "duration": row[4],
            "danger": row[5],
            "type": row[6]
        })

    return result

from fastapi import HTTPException

# POST endpoint to create a new event
@app.post("/events")
def create_event(event: dict):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO events (id, place, city, date, duration, danger, type)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                event["id"],
                event["place"],
                event["city"],
                event["date"],
                event["duration"],
                event["danger"],
                event["type"]
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {"status": "created"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 

# CORRESPONDENT ENDPOINTS
@app.get("/correspondents")
def get_correspondents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM correspondent;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "country": row[2],
            "city": row[3],
            "specification": row[4],
            "operator": row[5],
            "price": float(row[6])
        })
    return result

@app.post("/correspondents")
def create_correspondent(correspondent: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO correspondent (id, name, country, city, specification, operator, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                correspondent["id"],
                correspondent["name"],
                correspondent["country"],
                correspondent["city"],
                correspondent["specification"],
                correspondent["operator"],
                correspondent["price"]
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"status": "created"}


# REPORT ENDPOINTS
@app.get("/reportages")
def get_reportages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reportage;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "date": row[1],
            "quality": row[2],
            "time": str(row[3]),
            "video": row[4],
            "event_id": row[5],
            "correspondent_id": row[6]
        })
    return result

@app.post("/reportages")
def create_reportage(reportage: dict):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO reportage (id, date, quality, time, video, event_id, correspondent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                reportage["id"],
                reportage["date"],
                reportage["quality"],
                reportage["time"],
                reportage["video"],
                reportage["event_id"],
                reportage["correspondent_id"]
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
    return {"status": "created"}