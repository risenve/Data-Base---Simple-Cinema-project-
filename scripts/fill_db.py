import requests
import random
from datetime import datetime, timedelta


BASE_URL = "http://127.0.0.1:8000"

cities = ["Yerevan", "Gyumri", "Vanadzor", "Dilijan", "Ashtarak"]
places = ["Central Square", "Opera Theater", "Republic Square", "Cascade", "Sports Complex"]
danger_levels = ["low", "medium", "high"]
event_types = ["protest", "concert", "exhibition", "sport", "conference"]
qualities = ["HD", "FullHD", "4K"]

def create_event():
    """Создать случайное событие"""
    event_data = {
        "place": random.choice(places),
        "city": random.choice(cities),
        "date": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
        "duration": random.randint(30, 240),
        "danger": random.choice(danger_levels),
        "type": random.choice(event_types),
        "extra_metadata": {
            "attendance": random.randint(50, 5000),
            "organizer": f"Org_{random.randint(1, 100)}",
            "notes": f"Event note #{random.randint(1, 1000)}",
            "priority": random.choice(["low", "medium", "high"])
        }
    }
    
    response = requests.post(f"{BASE_URL}/events/", json=event_data)
    if response.status_code == 201 or response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating event: {response.text}")
        return None

def create_correspondent():
    """Создать случайного корреспондента"""
    names = ["Anna", "John", "Maria", "David", "Sophia", "Michael", "Elena", "Alex"]
    surnames = ["Smith", "Johnson", "Brown", "Wilson", "Taylor", "Clark", "Lee", "Walker"]
    
    correspondent_data = {
        "name": f"{random.choice(names)} {random.choice(surnames)}",
        "country": "Armenia",
        "city": random.choice(cities),
        "specification": random.choice(["war", "politics", "culture", "sport", "economics"]),
        "operator": random.choice([True, False]),
        "price": round(random.uniform(50.0, 500.0), 2)
    }
    
    response = requests.post(f"{BASE_URL}/correspondents/", json=correspondent_data)
    if response.status_code == 201 or response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating correspondent: {response.text}")
        return None

def create_reportage(event_id, correspondent_id):
    """Создать репортаж"""
    reportage_data = {
        "date": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
        "quality": random.choice(qualities),
        "time": f"{random.randint(8, 22)}:{random.randint(0, 59):02d}",
        "video": random.choice([True, False]),
        "event_id": event_id,
        "correspondent_id": correspondent_id
    }
    
    response = requests.post(f"{BASE_URL}/reportages/", json=reportage_data)
    if response.status_code == 201 or response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating reportage: {response.text}")
        return None

def main():
    print("Starting to fill database with sample data...")
    
    # creating 20 events
    event_ids = []
    for i in range(20):
        print(f"Creating event {i+1}/20...")
        event_id = create_event()
        if event_id:
            event_ids.append(event_id)
    
    # creating 15 correspondents
    correspondent_ids = []
    for i in range(15):
        print(f"Creating correspondent {i+1}/15...")
        correspondent_id = create_correspondent()
        if correspondent_id:
            correspondent_ids.append(correspondent_id)
    
    # creating 30 reportages (with refereces)
    for i in range(30):
        print(f"Creating reportage {i+1}/30...")
        if event_ids and correspondent_ids:
            event_id = random.choice(event_ids)
            correspondent_id = random.choice(correspondent_ids)
            create_reportage(event_id, correspondent_id)
    
    print("\n Database filling completed!")
    print(f"Created: {len(event_ids)} events, {len(correspondent_ids)} correspondents, 30 reportages")
    print(f"API available at: {BASE_URL}/docs")

if __name__ == "__main__":
    main()