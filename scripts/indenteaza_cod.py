import json
import re

def indent_code(fragment: str, indent_str='    '):
    lines = fragment.split('\n')
    indent_level = 0
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('}'):
            indent_level = max(indent_level - 1, 0)
        new_lines.append(indent_str * indent_level + stripped)
        if '{' in stripped and not stripped.startswith('//'):
            indent_level += stripped.count('{')
        if '}' in stripped:
            indent_level = max(indent_level - stripped.count('}'), 0)
    return '\n'.join(new_lines)

def process_text(text: str) -> str:
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        if re.match(r'^\s*(#|void|int|float|char|double|class)\b', line):
            prelude = lines[:idx]
            code = '\n'.join(lines[idx:])
            return '\n'.join(prelude) + '\n' + indent_code(code)
    return text

def process_data(obj):
    if isinstance(obj, dict):
        return {k: process_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [process_data(item) for item in obj]
    elif isinstance(obj, str):
        if '\n' in obj:
            return process_text(obj)
        return obj
    else:
        return obj

def main():
    with open('../assets/grile_fara_indentare.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed = process_data(data)

    with open('../assets/grile.json', 'w', encoding='utf-8') as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
