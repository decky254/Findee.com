import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# 🧠 AI QUERY CLASSIFIER
# -----------------------------
def analyze_query(text, location):

    prompt = f"""
    You are a search classification engine.

    Convert user input into JSON ONLY with:
    - category (Jobs, Business, Trading, Education, Tech, etc.)
    - subcategory (Remote, Local, Forex, Networking, etc.)
    - intent_summary

    User input: {text}
    Location: {location}

    Return ONLY valid JSON.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)


# -----------------------------
# 💡 DID YOU KNOW GENERATOR
# -----------------------------
def generate_did_you_know(category):

    prompt = f"""
    Create 3 short "Did you know?" insights about {category}.
    Focus on:
    - online communities
    - money-making opportunities
    - useful digital trends

    Keep each line short.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.split("\n")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.split("\n")
