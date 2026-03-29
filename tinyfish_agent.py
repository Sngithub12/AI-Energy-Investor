import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://agent.tinyfish.ai/v1/automation/run-sse"

def get_companies_for_country(country, query):

    goal = f"""
    Search for companies in {country} related to: {query}.
    
    Return ONLY in JSON format like:
    [
      {{"company": "Company Name", "description": "What they do"}},
      {{"company": "Company Name", "description": "What they do"}}
    ]
    """

    try:
        response = requests.post(
            API_URL,
            headers={
                "X-API-Key": os.getenv("TINYFISH_API_KEY"),
                "Content-Type": "application/json",
            },
            json={
                "url": "https://www.google.com",
                "goal": goal
            },
            stream=True
        )

        full_output = ""

        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                print(decoded)  # optional debug
                full_output += decoded

        # 🔥 Try extracting JSON from output
        start = full_output.find("[")
        end = full_output.rfind("]")

        if start != -1 and end != -1:
            json_str = full_output[start:end+1]
            return json.loads(json_str)

        return []

    except Exception as e:
        print("❌ TinyFish Error:", e)
        return []
def build_goal(country, query):
    return f"""
    Find companies based on this query:

    Query: {query}
    Country: {country}

    Extract:
    - Top companies
    - Description
    - Industry relevance

    Return clean structured results.
    """