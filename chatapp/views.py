import random
import csv
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils.crypto import get_random_string
from firebase_admin import db
import threading
import time
import json
import os
from django.conf import settings

# Path to your CSV file containing names
NAMES_CSV_PATH = os.path.join(settings.BASE_DIR, 'static\media\LastNames.csv')

# Load names from CSV into a list
with open(NAMES_CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    names_list = list(reader)

# Function to clear the database every 12 hours
def clear_database():
    while True:
        time.sleep(43200)  # 12 hours in seconds
        ref = db.reference('/')
        ref.set({})

threading.Thread(target=clear_database, daemon=True).start()

def join_group(request):
    if request.method == 'POST':
        # Generate a random name from the loaded names list
        username = random.choice(names_list)[0]  # Assuming the CSV has names in the first column

        # Generate a random character (or use a predefined set)
        character = get_random_string(1)

        # Store username and character in session
        request.session['username'] = username
        request.session['character'] = character

        return redirect('chat')

    return render(request, 'join_group.html')

def chat(request):
    if 'username' not in request.session:
        return redirect('join_group')

    firebase_config_path = os.path.join(settings.BASE_DIR, 'serviceAccountKey.json')
    with open(firebase_config_path) as f:
        service_account_key = json.load(f)

    # Construct the Firebase config object for the front-end
    firebase_config = {
        "apiKey": "332590759bfdff895137d555195cc1a23d8128ba",
        "authDomain": f"{service_account_key['project_id']}.firebaseapp.com",
        "databaseURL": "https://chatapp-ddb2e-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": service_account_key['project_id'],
        "storageBucket": f"{service_account_key['project_id']}.appspot.com",
        "messagingSenderId": "your-messaging-sender-id",
        "appId": "chatapp-ddb2e"
    }

    return render(request, 'chat.html', {
        'username': request.session['username'],
        'character': request.session['character'],
        'firebase_config': json.dumps(firebase_config)  # Pass as JSON string
    })

def logout_view(request):
    logout(request)
    return redirect('join_group')

def profile_page(request):
    return render(request, 'profile.html')
