# utils.py
import re
import fitz  # PyMuPDF
from docx import Document

# Allowed Tajik characters
allowed_chars = "ёйқукенгшҳзхъфҷвапролджэячсмитӣбюғӯЁЙҚУКЕНГШҲЗХЪФҶВАПРОЛДЖЭЯЧСМИТӢБЮҒӮ?.,"

# Incorrect -> Correct Tajik letters
fix_tajik_letters = {
    "r": "к",
    "ў": "ӯ",
    "љ": "ҷ",
    "Ї": "Ӣ",
    "ќ": "қ",
    "њ": "ҳ",
    "Ё": "Е",
    "E": "Е",
    "Ў": "Ӯ",
    "Ќ": "Қ",
    "c": "с",
    "ї": "ӣ",
    "Њ": "Ҳ",
    "Љ": "Ҷ",
    "Ѓ": "Ғ",
    "ѓ": "ғ"
}

def fix_sentence(sentence):
    return ''.join(fix_tajik_letters.get(char, char) for char in sentence)

def is_valid_sentence(sentence):
    for char in sentence:
        if char not in allowed_chars and not char.isspace():
            return False
    words = sentence.strip().split()
    return 3 < len(words) <= 15

def remove_initial_uppercase(sentence):
    words = sentence.split()
    new_words = []
    found_real_start = False

    for word in words:
        if not word.isupper() or len(word) <= 2:
            found_real_start = True
        if found_real_start:
            new_words.append(word)
    return ' '.join(new_words)

def read_and_filter_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    sentences = re.findall(r'[^.?\n]+[.?]', text)

    filtered_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        sentence = fix_sentence(sentence)
        sentence = remove_initial_uppercase(sentence)
        if is_valid_sentence(sentence):
            filtered_sentences.append(sentence)

    return filtered_sentences

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return ' '.join(page.get_text() for page in doc)

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join(para.text for para in doc.paragraphs)
