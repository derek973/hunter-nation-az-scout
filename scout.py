import os
import requests
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
webhook = os.environ["SLACK_WEBHOOK_URL"]

today = datetime.now().strftime("%A, %B %d, %Y")
report_id = datetime.now().strftime("%Y%m%d")

prompt = f"""
You are SCOUT, the Arizona hunting intelligence agent for Hunter Nation Arizona.

Create a high-signal Arizona-only hunting intelligence report.

Rules:
- Only include NEW or materially changed items in the last 72 hours
- Skip topics with no updates
- No filler
- No markdown

Focus on:
- Arizona Game and Fish
- Mexican gray wolf
- Chronic Wasting Disease
- Public land access
- Predator management
- Anti-hunting threats
- Arizona legislation
- Federal actions impacting Arizona

Format:

HUNTER NATION ARIZONA - SCOUT INTEL REPORT | {today} | Report #{report_id}

Topic — NEW or ONGOING
What happened. One or two sentences max.
Why it matters to AZ hunters. One sentence.
Source: [full URL]
"""

response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search"}],
    input=prompt
)

report = response.output_text

requests.post(webhook, json={"text": report})
