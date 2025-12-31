import requests
import random
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv


API_PORT = os.environ.get("API_PORT", "8000")
BASE_URL = f"http://localhost:{API_PORT}"

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
    if response.status_code in [200, 201]:
        return response.json()["id"]
    else:
        print(f"Error creating event: {response.status_code} - {response.text[:100]}")
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
    if response.status_code in [200, 201]:
        return response.json()["id"]
    else:
        print(f"Error creating correspondent: {response.status_code} - {response.text[:100]}")
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
    if response.status_code in [200, 201]:
        return response.json()["id"]
    else:
        print(f"Error creating reportage: {response.status_code} - {response.text[:200]}")
        return None

def main():
    print("Starting to fill database with sample data...")
    
    # 20 events 
    event_ids = []
    for i in range(20):
        print(f"Creating event {i+1}/20...")
        event_id = create_event()
        if event_id:
            event_ids.append(event_id)
        else:
            print("  Skipping...")
    
    # 15 correspondents
    correspondent_ids = []
    for i in range(15):
        print(f"Creating correspondent {i+1}/15...")
        correspondent_id = create_correspondent()
        if correspondent_id:
            correspondent_ids.append(correspondent_id)
        else:
            print("  Skipping...")
    
    print(f"\nCreated {len(event_ids)} events and {len(correspondent_ids)} correspondents")
    
    created_reportages = 0

    if event_ids and correspondent_ids:
        reportage_count = min(30, len(event_ids) * len(correspondent_ids))
        print(f"Creating {reportage_count} reportages...")
        
        created_reportages = 0
        for i in range(reportage_count):
            print(f"Creating reportage {i+1}/{reportage_count}...")
            event_id = random.choice(event_ids)
            correspondent_id = random.choice(correspondent_ids)
            
            if create_reportage(event_id, correspondent_id):
                created_reportages += 1
    else:
        print("Cannot create reportages - missing events or correspondents")
    
    print(f"\n✅ Database filling completed!")
    print(f"Created: {len(event_ids)} events, {len(correspondent_ids)} correspondents, {created_reportages} reportages")
    print(f"API available at: {BASE_URL}/docs")

if __name__ == "__main__":
    main()