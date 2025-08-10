import re
from typing import List

def extract_questions(text:str)->List:
    pattern = r'^\s*\d+[\.\)]\s*(.+?\?)'
    matches = re.findall(pattern, text, flags=re.MULTILINE | re.DOTALL)
    cleaned_questions = []
    for q in matches:
        # Strip whitespace
        q_strip = q.strip()
        # Remove numbering like '1. ' or '2) '
        cleaned = re.sub(r'^\s*\d+[\.\)]\s*', '', q_strip)
        cleaned_questions.append(cleaned)
    return cleaned_questions


