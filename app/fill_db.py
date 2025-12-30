import requests

BASE_URL = "http://127.0.0.1:8000"
# adding events
events = [
    {
        "place": "Central Square",
        "city": "Yerevan",
        "date": "2024-10-12",
        "duration": 120,
        "danger": "low",
        "type": "protest"
    },
    {
        "place": "Opera Theater",
        "city": "Yerevan",
        "date": "2024-10-13",
        "duration": 90,
        "danger": "medium",
        "type": "concert"
    }
]

for event in events:
    response = requests.post(f"{BASE_URL}/events", json=event)
    print(response.json())
# adding correspondents 
correspondents = [
    {
        "name": "Anna Smith",
        "country": "Armenia",
        "city": "Yerevan",
        "specification": "war",
        "operator": True,
        "price": 150.0
    },
    {
        "name": "John Doe",
        "country": "Armenia",
        "city": "Gyumri",
        "specification": "politics",
        "operator": False,
        "price": 100.0
    }
]

for c in correspondents:
    response = requests.post(f"{BASE_URL}/correspondents", json=c)
    print(response.json())

# adding reportages
reportages = [
    {
        "date": "2024-10-12",
        "quality": "HD",
        "time": "18:30",
        "video": True,
        "event_id": 1,
        "correspondent_id": 1
    },
    {
        "date": "2024-10-13",
        "quality": "FullHD",
        "time": "20:00",
        "video": True,
        "event_id": 2,
        "correspondent_id": 2
    }
]

for r in reportages:
    response = requests.post(f"{BASE_URL}/events", json=event)
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)