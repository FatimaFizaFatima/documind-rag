import re
import unicodedata

def clean_data(text: str) -> str:
    
    text = unicodedata.normalize("NFKC", text)

    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    text = re.sub(r'[ \t]+', ' ', text)

    text = re.sub(r'[ \t]\n', '\n', text)

    text = re.sub(r'\n{3,}', '\n\n', text)

    text = text.strip()

    return text