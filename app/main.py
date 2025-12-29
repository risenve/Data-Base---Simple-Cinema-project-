from fastapi import FastAPI
import psycopg2
import os

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

# Adding an endpoint to create a new event
from fastapi import HTTPException

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