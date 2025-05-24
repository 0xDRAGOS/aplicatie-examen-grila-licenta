import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_explanation(question):
    text = f"Provide a short explanation for the following multiple choice question:\n\n"
    text += f"Question: {question['text']}\n"
    for key, val in question.get("options", {}).items():
        text += f"{key}. {val}\n"
    correct = question["correct_answer"]
    correct_text = ", ".join(correct) if isinstance(correct, list) else correct
    text += f"\nCorrect answer: {correct_text}\n"
    text += "Explanation:"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

with open("../assets/grile.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for subject in data.get("subjects", []):
    for question in subject.get("questions", []):
        if not question.get("explanation"):
            try:
                explanation = generate_explanation(question)
                question["explanation"] = explanation
                print(f"✓ Explicație generată pentru: {question['text'][:60]}...")
            except Exception as e:
                print(f"✗ Eroare la întrebarea: {question['text'][:60]}... => {e}")

with open("../assets/grile2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Gata! Toate explicațiile au fost generate.")
