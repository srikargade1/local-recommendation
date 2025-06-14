import json
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv() 

openai_client = OpenAI(api_key= os.environ.get("OPENAI_API_KEY"))
 # or pass api_key='...' if needed

def parse_prompt_to_filters(prompt):
    system_msg = (
        "You are an assistant that converts user travel-related queries into JSON filter objects "
        "for place search. Only return the JSON object. Available fields are:\n"
        "- query (string)\n"
        "- open_now (boolean)\n"
        "- max_price (integer, 1-4)\n"
        "- exclude_chains (boolean)\n"
        "- radius_meters (integer in meters, optional)\n"
        "Do not include any text outside the JSON."
    )

    user_msg = f"User prompt: {prompt}"

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    try:
        filters = json.loads(raw)
        print("🔍 Parsed filters:", filters)
        return filters
    except json.JSONDecodeError:
        print("❌ Failed to parse GPT response:")
        print(raw)
        return {
        "query": prompt,
        "open_now": False,
        "exclude_chains": False,
        "radius_meters": 1000
    }
