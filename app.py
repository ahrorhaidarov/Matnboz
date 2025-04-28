import streamlit as st
import io

from utils import read_and_filter_sentences



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
            st.code(result_text, language='text', height=300)

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
