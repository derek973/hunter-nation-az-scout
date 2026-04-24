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
- Only include NEW or materially changed items from the last 72 hours.
- Skip topics with no meaningful updates.
- No filler.
- No markdown.
- Every item must include a source URL.
- Only include Arizona-specific items or federal/regional items that clearly affect Arizona.

Monitor:
- Mexican gray wolf
- Chronic Wasting Disease
- Arizona Game and Fish Commission
- Public land access
- OHV and hunting access
- Predator management
- Anti-hunting threats
- Federal wildlife decisions
- Hunter Nation Arizona / Hunter Nation national signals affecting Arizona

Prioritize:
azgfd.gov, fws.gov, fs.usda.gov, blm.gov/arizona, azleg.gov, federalregister.gov,
hunternation.org, rmef.org, backcountryhunters.org, biologicaldiversity.org,
humanesociety.org, earthjustice.org, azcentral.com, tucson.com, azcapitoltimes.com

Format exactly:

HUNTER NATION ARIZONA - SCOUT INTEL REPORT | {today} | Report #{report_id}

Topic Name — NEW or ONGOING
What happened. One or two sentences max.
Why it matters to AZ hunters. One sentence.
Source: [full URL]

If nothing new is found, say:
HUNTER NATION ARIZONA - SCOUT INTEL REPORT | {today} | Report #{report_id}

No material Arizona hunting intelligence updates found in the last 72 hours.
"""

response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search"}],
    input=prompt
)

report = response.output_text.strip()

slack_response = requests.post(webhook, json={"text": report})
print(slack_response.status_code)
print(slack_response.text)
