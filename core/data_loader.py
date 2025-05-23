import json


def load_subjects(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('subjects', [])
    except Exception as e:
        print(f"Eroare la incarcarea fisierului JSON: {e}")
        return []
