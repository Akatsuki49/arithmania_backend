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

# Fetch data for the particular user
user_data = ref.document(user_id).collection("transactions").get()

# Display data for the particular user
if user_data:
    print("Data for user with ID", user_id, ":")
    for doc in user_data:
        print("Document ID:", doc.id)
        # Access data within the document
        data = doc.to_dict()
        for key, value in data.items():
            print(key, ":", value)
else:
    print("User with ID", user_id, "not found.")
