import re
import io

# Харфҳои иҷозатдодашуда
allowed_chars = "ёйқукенгшҳзхъфҷвапролджэячсмитӣбюғӯЁЙҚУКЕНГШҲЗХЪФҶВАПРОЛДЖЭЯЧСМИТӢБЮҒӮ?.,"

# Ислоҳ кардани ҳарфҳои нодуруст
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
    fixed = ""
    for char in sentence:
        if char in fix_tajik_letters:
            fixed += fix_tajik_letters[char]
        else:
            fixed += char
    return fixed

def is_valid_sentence(sentence):
    for char in sentence:
        if char not in allowed_chars and not char.isspace():
            return False
    words = sentence.strip().split()
    return len(words) <= 15 and len(words) > 3

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

