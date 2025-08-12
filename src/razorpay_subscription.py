import requests
from requests.auth import HTTPBasicAuth

# ---------------- CONFIG ----------------
RAZORPAY_KEY_ID = ""
RAZORPAY_KEY_SECRET = ""
CANCEL_AT_CYCLE_END = False  # True = cancel at cycle end, False = cancel immediately
# -----------------------------------------

BASE_URL = "https://api.razorpay.com/v1"

def fetch_subscriptions_by_status(status):
    """
    Fetch subscriptions by status.
    Handles pagination if there are more than 100.
    """
    all_ids = []
    skip = 0
    while True:
        url = f"{BASE_URL}/subscriptions"
        params = {
            "status": status,
            "count": 100,
            "skip": skip
        }
        response = requests.get(url, params=params, auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        if response.status_code != 200:
            print(f"Error fetching {status} subscriptions:", response.text)
            break

        data = response.json().get("items", [])
        if not data:
            break

        ids = [sub["id"] for sub in data]
        all_ids.extend(ids)

        if len(data) < 100:  # No more pages
            break
        skip += 100

    return all_ids

def cancel_subscription(subscription_id):
    """
    Cancel a specific subscription.
    """
    url = f"{BASE_URL}/subscriptions/{subscription_id}/cancel"
    payload = {
        "cancel_at_cycle_end": CANCEL_AT_CYCLE_END
    }
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    if response.status_code == 200:
        print(f"✅ Cancelled: {subscription_id}")
    else:
        print(f"❌ Failed to cancel {subscription_id}: {response.text}")

def bulk_cancel_subscriptions():
    active_subs = fetch_subscriptions_by_status("active")
    created_subs = fetch_subscriptions_by_status("created")
    authenticated_subs = fetch_subscriptions_by_status("authenticated")

    all_subs = list(set(active_subs + created_subs + authenticated_subs))  # remove duplicates
    if not all_subs:
        print("No active or created subscriptions found.")
        return

    print(f"Found {len(all_subs)} subscriptions to cancel.")
    for sub_id in all_subs:
        cancel_subscription(sub_id)

if __name__ == "__main__":
    bulk_cancel_subscriptions()
