from datetime import datetime, timedelta
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Fetch the service account key JSON file contents
cred = credentials.Certificate(
    'arithmania2024-firebase-adminsdk-zm0t4-f8224e467a.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

db = firestore.client()

# Reference to the "users" collection
ref = db.collection('users')

user_id = "joocollan2byMASmVb8NlPnYJO12"

# Function to generate random timestamp within a range


def random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    return start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)


# Generate random timestamps for the last year
start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

dummy_data = [
    {"amount": 100.0, "type": "expense", "category": "groceries",
        "description": "Grocery shopping", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 50.0, "type": "expense", "category": "dining",
        "description": "Dinner with friends", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 200.0, "type": "expense", "category": "utilities",
        "description": "Electricity bill", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 150.0, "type": "income", "category": "salary",
        "description": "Monthly salary", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 75.0, "type": "expense", "category": "transportation",
        "description": "Fuel for car", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 40.0, "type": "expense", "category": "entertainment",
        "description": "Movie tickets", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 20.0, "type": "expense", "category": "shopping",
        "description": "Online shopping", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 300.0, "type": "income", "category": "bonus",
        "description": "Year-end bonus", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 120.0, "type": "expense", "category": "healthcare",
        "description": "Medicines", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 90.0, "type": "expense", "category": "subscriptions",
        "description": "Monthly subscriptions", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 80.0, "type": "expense", "category": "dining",
        "description": "Lunch with colleagues", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 250.0, "type": "expense", "category": "utilities",
        "description": "Water bill", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 180.0, "type": "expense", "category": "shopping",
        "description": "Clothing purchase", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 60.0, "type": "expense", "category": "entertainment",
        "description": "Concert tickets", "timestamp": random_timestamp(start_date, end_date)},
    {"amount": 200.0, "type": "income", "category": "salary",
        "description": "Part-time job payment", "timestamp": random_timestamp(start_date, end_date)},
]

# Push dummy data to Firestore
for data in dummy_data:
    ref.document(user_id).collection("transactions").add(data)

print("Dummy data added successfully.")
# # Fetch data for the particular user
# user_data = ref.document(user_id).collection("transactions").get()

# # Display data for the particular user
# if user_data:
#     print("Data for user with ID", user_id, ":")
#     for doc in user_data:
#         print("Document ID:", doc.id)
#         # Access data within the document
#         data = doc.to_dict()
#         for key, value in data.items():
#             print(key, ":", value)
# else:
#     print("User with ID", user_id, "not found.")
