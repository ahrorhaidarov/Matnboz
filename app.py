import streamlit as st
from utils import (
    read_and_filter_sentences,
    extract_text_from_pdf,
    extract_text_from_docx
)

st.set_page_config(page_title="Матнбоз - Филтркунии матнҳо", page_icon="📖", layout="centered")

# --- CSS Styling ---
st.markdown(
    """
    <style>
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

# --- Init session state ---
for key in ["input_text", "result_text", "filtered_sentences"]:
    st.session_state.setdefault(key, "")
st.session_state.setdefault("uploaded", False)
st.session_state.setdefault("uploader_key", 0)

# --- Title ---
st.title("📖 Матнбоз")
st.subheader("🎯 Барнома барои ҷудо ва филтр кардани ҷумлаҳо аз матнҳои PDF, DOCX ва матни дастӣ")

st.write('Бо истифода аз Матнбоз шумо метавонед матни файли PDF ё DOCX-ро хонда, ё матни дастӣ воридкардаро ба ҷумлаҳои ҷудо ва филтршударо табдил диҳед ва натиҷаҳоро дар шакли файл (.txt) захира кунед.')

# --- Upload / Input ---
st.markdown("### 📥 Ворид кардани матн ё боркунии файл")

uploaded_file = st.file_uploader(
    "📎 Файли худро (.pdf ё .docx) бор кунед:",
    type=["pdf", "docx"],
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded_file:
    st.session_state.uploaded = True

# If no file is uploaded, show text input
if not st.session_state.uploaded:
    manual_input = st.text_area("✏️ Ё матни худро дастӣ ворид кунед:", height=200)

# --- START Processing ---
if st.button("🔍 Ҷудокунии Ҷумлаҳо"):
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            st.session_state.input_text = extract_text_from_pdf(uploaded_file)
            st.info("📄 Матн аз файли PDF хонда шуд.")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.session_state.input_text = extract_text_from_docx(uploaded_file)
            st.info("📄 Матн аз файли DOCX хонда шуд.")
        st.session_state.uploaded = False
    elif not st.session_state.uploaded and 'manual_input' in locals() and manual_input.strip():
        st.session_state.input_text = manual_input
        st.info("📝 Матн аз саҳфаи воридгардида хонда шуд.")
    else:
        st.warning("⚠️ Лутфан аввал матн ворид кунед ё файл бор кунед!")

    # Process the input text
    if st.session_state.input_text.strip():
        filtered = read_and_filter_sentences(st.session_state.input_text)
        st.session_state.filtered_sentences = filtered
        st.session_state.result_text = "\n".join(filtered)

# --- Results ---
if st.session_state.filtered_sentences:
    st.markdown("### ✅ Ҷумлаҳои филтршуда:")
    st.code(st.session_state.result_text, language="text", height=300)

    st.download_button(
        label="⬇️ Боргирии натиҷаҳо",
        data=st.session_state.result_text.encode("utf-8"),
        file_name="натиҷа.txt",
        mime="text/plain"
    )

    # --- Reset ---
    if st.button("🔁 Оғози нав"):
        for key in ["input_text", "result_text", "filtered_sentences"]:
            st.session_state[key] = ""
        st.session_state.uploaded = False
        st.session_state.uploader_key += 1  # force file_uploader to reset
        st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("🚀 Лоиҳа аз ҷониби Аҳрорҷон Ҳ. • Барои забони тоҷикӣ 🇹🇯")
st.caption("Алоқа: alanjon1312@gmail.com")
