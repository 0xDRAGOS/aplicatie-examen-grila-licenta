import json
import re

# Detect blocuri pentru Java, HTML și PHP
JAVA_KEYWORDS = r'(void|int|float|char|double|class|public|private|protected|static|if|for|while|switch)'
HTML_TAG_PATTERN = re.compile(r'<[^/>]+?>|</[^>]+?>')
PHP_PATTERN = re.compile(r'<\?php|\?>|function|if|else|foreach|while')

def indent_code(fragment: str, indent_str='    '):
    lines = fragment.split('\n')
    indent_level = 0
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('}') or stripped.startswith('</') or stripped == '?>':
            indent_level = max(indent_level - 1, 0)
        new_lines.append(indent_str * indent_level + stripped)
        if ('{' in stripped and not stripped.startswith('//')) or re.match(r'<[^/!][^>]*>', stripped) or stripped == '<?php':
            indent_level += 1
        if '}' in stripped or re.match(r'</[^>]+>', stripped):
            indent_level = max(indent_level - 1, 0)
    return '\n'.join(new_lines)

def is_java_code(text: str) -> bool:
    return bool(re.search(JAVA_KEYWORDS, text))

def is_html_code(text: str) -> bool:
    return bool(HTML_TAG_PATTERN.search(text))

def is_php_code(text: str) -> bool:
    return bool(PHP_PATTERN.search(text))

def process_text(text: str) -> str:
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        if re.match(r'^\s*(#|void|int|float|char|double|class|public|<|<\?php)', line):
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
        if '\n' in obj and (is_java_code(obj) or is_html_code(obj) or is_php_code(obj)):
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