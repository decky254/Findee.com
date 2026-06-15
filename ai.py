import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_query(text, location):

    prompt = f"""
    You are a search classification AI.

    Convert user input into JSON with:
    - category
    - subcategory
    - intent summary
    - suggested_filters

    User input: {text}
    Location: {location}

    Return ONLY valid JSON.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)


def generate_did_you_know(category):
    prompt = f"""
    Generate 3 short "Did you know?" insights about {category}.
    Make them engaging, practical, and based on online communities and opportunities.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.split("\n")
