import requests
import time
from datetime import datetime
import json
from dotenv import load_dotenv
import os
load_dotenv()


# ----- CONFIGURATION -----
ONESIGNAL_APP_ID = 'YOUR_ONESIGNAL_APP_ID'  # Your OneSignal App ID
ONESIGNAL_REST_API_KEY = os.getenv('ONESIGNAL_REST_API_KEY')
PUSHENGAGE_API_KEY = os.getenv('PUSHENGAGE_API_KEY')
PUSHENGAGE_SEGMENT_ID = '144191'

BATCH_SIZE = 50  # Start with 50 to test PushEngage

# API Endpoints
ONESIGNAL_DEVICES_ENDPOINT = 'https://onesignal.com/api/v1/players'
PUSHENGAGE_SEGMENT_ENDPOINT = 'https://api.pushengage.com/apiv1/segments/addSegmentWithHash'


def get_onesignal_subscribers(app_id, api_key, limit=50, offset=0):
    """
    Fetches subscribers from OneSignal API.
    """
    headers = {
        'Authorization': f'Basic {api_key}',
        'Content-Type': 'application/json'
    }

    params = {
        'app_id': app_id,
        'limit': limit,
        'offset': offset
    }

    try:
        print(f"📡 Fetching {limit} subscribers from OneSignal (offset: {offset})...")
        response = requests.get(ONESIGNAL_DEVICES_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        subscribers = data.get('players', [])

        print(f"✅ Retrieved {len(subscribers)} subscribers.")
        return subscribers
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching OneSignal subscribers: {e}")
        if hasattr(e.response, 'text'):
            print(f"🔍 Error details: {e.response.text}")
        return None


def add_subscribers_to_pushengage(segment_id, subscribers, api_key):
    """
    Adds subscribers to PushEngage segment.
    """
    if not subscribers:
        print("⚠️ No subscribers to add. Skipping import.")
        return None

    data = {'segment_id': segment_id}
    for idx, sub_hash in enumerate(subscribers):
        data[f'subscriber_hash[{idx}]'] = sub_hash

    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    print(f"\n📤 Sending batch of {len(subscribers)} subscribers to PushEngage...")
    time.sleep(0.5)  # 🚀 Subtle rate limit

    try:
        response = requests.post(PUSHENGAGE_SEGMENT_ENDPOINT, data=data, headers=headers)
        print(f"📥 PushEngage Response: {response.text}")  # Print API response
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error adding subscribers to PushEngage: {e}")
        if hasattr(e.response, 'text'):
            print(f"🔍 Error details: {e.response.text}")
        return None


def main():
    print(f"🚀 Starting migration at {datetime.now()}")

    # Fetch first batch (50 subscribers) and test importing
    subscribers = get_onesignal_subscribers(ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY, BATCH_SIZE, 0)

    if not subscribers:
        print("⚠️ No subscribers found. Exiting...")
        return

    # Extract active subscribers (filter valid ones)
    active_subscribers = {
        sub.get('id') for sub in subscribers if sub.get('id') and sub.get('subscribed', True)
    }

    print(f"🟢 Found {len(active_subscribers)} active subscribers in first batch.")

    # ✅ Import first batch immediately to test PushEngage
    print("\n🔄 Attempting first import to PushEngage...")
    result = add_subscribers_to_pushengage(PUSHENGAGE_SEGMENT_ID, list(active_subscribers), PUSHENGAGE_API_KEY)

    if result and result.get('success'):
        print("✅ First batch imported successfully! Continuing migration...\n")
    else:
        print("❌ First batch import failed. Check API response and fix errors before proceeding.")
        return  # Stop execution if first import fails

    # ✅ If first batch worked, continue fetching/importing in chunks
    offset = BATCH_SIZE
    total_migrated = len(active_subscribers)

    while True:
        time.sleep(1)  # 🚀 Subtle rate limit
        print(f"\n📡 Fetching next batch from offset {offset}...")

        subscribers = get_onesignal_subscribers(ONESIGNAL_APP_ID, ONESIGNAL_REST_API_KEY, BATCH_SIZE, offset)

        if not subscribers:
            print("✅ All subscribers processed.")
            break

        # Filter valid subscribers
        active_subscribers = {
            sub.get('id') for sub in subscribers if sub.get('id') and sub.get('subscribed', True)
        }

        print(f"🟢 Found {len(active_subscribers)} active subscribers in this batch.")

        if not active_subscribers:
            break  # Stop if no more valid subscribers

        # Import to PushEngage
        result = add_subscribers_to_pushengage(PUSHENGAGE_SEGMENT_ID, list(active_subscribers), PUSHENGAGE_API_KEY)

        if result and result.get('success'):
            total_migrated += len(active_subscribers)
            print(f"✅ Successfully imported batch. Total migrated so far: {total_migrated}")
        else:
            print(f"❌ Error importing batch at offset {offset}. Stopping.")
            break  # Stop if there's an error

        offset += BATCH_SIZE  # Move to the next batch

    print(f"\n🎉 Migration completed at {datetime.now()}")
    print(f"🔹 Total subscribers migrated: {total_migrated}")


if __name__ == "__main__":
    main()
