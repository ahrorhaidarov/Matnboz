import streamlit as st
import re
import io

# Харфҳои иҷозатдодашуда
allowed_chars = "ёйқукенгшҳзхъфҷвапролджэячсмитӣбюғӯЁЙҚУКЕНГШҲЗХЪФҷВАПРОЛДЖЭЯЧСМИТӢБЮҒӮ?.,"

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

# ---- Streamlit UI ----
st.set_page_config(page_title="Матнбоз - Филтркунии матнҳо", page_icon="📖", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: var(--bg-color, #f5f7fa);
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 10px;
        margin-top: 10px;
    }
    .stTextArea>div>div>textarea {
        background-color: var(--input-bg-color, #000000);
        color: var(--input-text-color, #ffffff);
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        width: 100%;
        min-height: 200px;
    }
    .stTextArea>div>div>textarea:focus {
        outline: none;
        box-shadow: 0 0 5px rgba(76, 175, 80, 0.7);
    }
    /* Define CSS variables for light and dark themes */
    :root {
        --bg-color: #f5f7fa;
        --input-bg-color: #ffffff;
        --input-text-color: #000000;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #0f172a;
            --input-bg-color: #000000;
            --input-text-color: #ffffff;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- Сарлавҳа ---
st.title("📖 Матнбоз")
st.subheader("🎯 Барнома барои ҷудо ва филтр кардани ҷумлаҳо аз матни калон")

st.write(
    "Бо истифода аз **Матнбоз** шумо метавонед аз матнҳои калон ҷумлаҳои мувофиқро ҷудо карда, "
    "онҳоро дар шакли файл (.txt) захира кунед."
)

# --- Матн ворид кардан ---
user_text = st.text_area("✏️ Матни худро дар ин ҷо ворид намоед:", height=300)

# --- Тугмаи Филтр кардан ---
if st.button("🔍 Ҷудокунии Ҷумлаҳо"):
    if user_text.strip() == "":
        st.warning("⚠️ Лутфан аввал матнро ворид кунед!")
    else:
        filtered = read_and_filter_sentences(user_text)

        if filtered:
            result_text = "\n".join(filtered)
            result_bytes = result_text.encode('utf-8')
            result_file = io.BytesIO(result_bytes)

            st.success(f"✅ Ҷумлаҳои филтршуда: {len(filtered)} адад.")
            # Display the result
            with st.container(height=300):
                st.code(result_text, language='text')

            st.download_button(
                label="⬇️ Боргирии натиҷаҳо",
                data=result_file,
                file_name="натиҷа.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Ҷумлаи мувофиқ ёфт нашуд.")

# --- Поён ---
st.markdown("---")
st.caption("🚀 Лоиҳа аз ҷониби Аҳрорҷон Ҳ. • Барои забони тоҷикӣ 🇹🇯 ")
st.caption("Алоқа: alanjon1312@gmail.com")
