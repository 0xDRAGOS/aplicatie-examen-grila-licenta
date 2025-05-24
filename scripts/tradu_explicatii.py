from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_to_romanian(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Tradu următorul text în limba română:\n\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

with open("../assets/grile2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Traduce explicațiile
for subject in data["subjects"]:
    for q in subject["questions"]:
        if "explanation" in q and q["explanation"]:
            q["explanation"] = translate_to_romanian(q["explanation"])

with open("../assets/grile_cu_explicatii_ro.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
