import requests
import json
import hashlib

import time
from dotenv import load_dotenv
import os
load_dotenv()


# ---- CONFIGURATION ----
ONESIGNAL_APP_ID = 'YOUR_ONESIGNAL_APP_ID'
ONESIGNAL_REST_API_KEY = os.getenv('ONESIGNAL_REST_API_KEY')
PUSHENGAGE_API_KEY = os.getenv('PUSHENGAGE_API_KEY')
PUSHENGAGE_SEGMENT_ID = '144191'

# API Endpoints
ONESIGNAL_DEVICES_ENDPOINT = 'https://onesignal.com/api/v1/players'
PUSHENGAGE_SEGMENT_ENDPOINT = 'https://api.pushengage.com/apiv1/segments/addSegmentWithHash'


def hash_subscriber(identifier):
    """ Convert subscriber identifier to SHA256 hash (required by PushEngage). """
    return hashlib.sha256(identifier.encode()).hexdigest()


def get_hashed_subscribers(subscribers):
    """ Convert all subscriber identifiers to SHA256 before sending. """
    return [hash_subscriber(sub) for sub in subscribers]


def get_onesignal_active_subscribers(app_id, api_key, limit=50):
    """
    Fetches at least 'limit' active subscribers from OneSignal API, filtering out invalid ones.
    """
    headers = {
        'Authorization': f'Basic {api_key}',
        'Content-Type': 'application/json'
    }
    params = {
        'app_id': app_id,
        'limit': limit,  # Fetch at least 'limit' subscribers
        'order': 'last_active'  # Sort by most recent activity
    }

    try:
        print(f"\n📡 Fetching {limit} recent subscribers from OneSignal...")
        response = requests.get(ONESIGNAL_DEVICES_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        total_subscribers = data.get('total_count', 0)
        fetched_subscribers = data.get('players', [])

        print(f"📊 Total Subscribers in OneSignal: {total_subscribers}")
        print(f"📥 Fetched {len(fetched_subscribers)} subscribers...")

        valid_subscribers = [
            s['identifier'] for s in fetched_subscribers
            if not s.get('invalid_identifier', False) and s.get('identifier')
        ]

        print(f"✅ Found {len(valid_subscribers)} valid subscribers.")
        return valid_subscribers
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching OneSignal subscribers: {e}")
        return []


def add_subscribers_to_pushengage(segment_id, subscribers, api_key, batch_size=5):
    """
    Adds subscribers to PushEngage segment using SHA256 hashed identifiers.
    """
    if not subscribers:
        print("⚠️ No valid subscribers to import.")
        return None

    hashed_subscribers = get_hashed_subscribers(subscribers)  # Convert identifiers to SHA256

    for i in range(0, len(hashed_subscribers), batch_size):
        batch = hashed_subscribers[i:i + batch_size]

        data = {'segment_id': segment_id}
        for idx, sub_hash in enumerate(batch):
            data[f'subscriber_hash[{idx}]'] = sub_hash

        headers = {
            'Api-Key': api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        print(f"\n📤 Sending batch of {len(batch)} subscribers to PushEngage...")
        print(json.dumps(data, indent=2)[:500])  # Print only first 500 chars

        try:
            response = requests.post(PUSHENGAGE_SEGMENT_ENDPOINT, data=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(f"📥 PushEngage Response: {response_data}")

            if not response_data.get('success'):
                print("❌ PushEngage reported failure.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding subscribers to PushEngage: {e}")
            return None

        time.sleep(2)  # Avoid hitting rate limits

    print("✅ Import process completed. Check PushEngage dashboard.")
    return True


# ---- RUN SCRIPT ----
if __name__ == "__main__":
    # Fetch at least 200 recent subscribers from OneSignal
    subscribers = get_onesignal_active_subscribers(ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY, limit=200)

    # If valid subscribers found, send them to PushEngage
    if subscribers:
        result = add_subscribers_to_pushengage(PUSHENGAGE_SEGMENT_ID, subscribers, PUSHENGAGE_API_KEY)

        if result:
            print("🎉 Success! Subscribers imported to PushEngage.")
        else:
            print("❌ Import failed! Debug needed.")
