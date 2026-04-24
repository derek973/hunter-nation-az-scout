import os
import requests

webhook = os.environ.get("SLACK_WEBHOOK_URL")

message = {
    "text": "🚨 SCOUT is live. Hunter Nation Arizona reporting in."
}

response = requests.post(webhook, json=message)

print(response.status_code)
