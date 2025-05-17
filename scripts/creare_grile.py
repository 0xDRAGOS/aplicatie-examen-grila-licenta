import pdfplumber
import re
import json
import warnings

PDF_PATH    = '../assets/pdf/licenta-2015-grile-modul-1.pdf'
OUTPUT_JSON = 'grile4_fixed.json'

warnings.filterwarnings('ignore', category=UserWarning, module='pdfplumber')


def extract_questions(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or '')
    full_text = '\n'.join(pages)

    subj_split = re.split(r'(?m)^\s*([123])\s+(.+?)\s*$', full_text)
    subjects = []
    it = iter(subj_split)
    next(it)
    for num, name, body in zip(it, it, it):
        name = name.strip()
        questions = []
        q_blocks = re.split(r'(?m)^\s*(\d+)\.\s*', body)[1:]
        for qid_str, block in zip(q_blocks[0::2], q_blocks[1::2]):
            qid = int(qid_str)
            parts = re.split(r'([A-E])\.\s*', block)
            qtext = parts[0].strip().replace('\n', ' ')
            options = {}
            for i in range(1, len(parts)-1, 2):
                key = parts[i]
                val = parts[i+1].strip().replace('\n', ' ')
                options[key] = val
            questions.append({
                'id': qid,
                'text': qtext,
                'options': options,
                'correct_answer': []
            })
        subjects.append({'name': name, 'questions': questions})
    return subjects

if __name__ == '__main__':
    data = extract_questions(PDF_PATH)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({'subjects': data}, f, ensure_ascii=False, indent=2)
    print(f'Fixed JSON written to {OUTPUT_JSON}')
