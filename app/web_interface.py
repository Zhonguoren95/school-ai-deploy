import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import pandas as pd
import io

st.set_page_config(page_title="AI-сервис подбора", layout="wide")
st.title("🤖 AI-сервис подбора оборудования")
st.markdown("Загрузите техническое задание и прайс-листы — система всё сделает сама.")

# Блок загрузки ТЗ
st.header("📄 Техническое задание")
uploaded_spec = st.file_uploader("Загрузите файл с ТЗ (PDF, DOCX)", type=["pdf", "docx"])

# Блок загрузки прайсов
st.header("📊 Прайсы поставщиков")
uploaded_prices = st.file_uploader("Загрузите 1 или несколько прайсов (Excel)", type=["xlsx"], accept_multiple_files=True)

# Функция обработки ТЗ
def extract_text_from_spec(file):
    if file.name.endswith(".pdf"):
        text = ""
        pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf_doc:
            text += page.get_text()
        return text
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    return ""

# Функция чтения прайсов
def read_prices(files):
    dfs = []
    for f in files:
        try:
            df = pd.read_excel(f)
            dfs.append(df)
        except:
            st.warning(f"Не удалось прочитать файл: {f.name}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# Кнопка запуска анализа
if st.button("🚀 Запустить подбор"):
    if uploaded_spec and uploaded_prices:
        st.success("Файлы получены! Идёт обработка...")

        spec_text = extract_text_from_spec(uploaded_spec)
        st.subheader("📜 Распознанный текст из ТЗ")
        st.text_area("", spec_text, height=300)

        df_prices = read_prices(uploaded_prices)
        st.subheader("📋 Объединённый прайс-лист")
        st.dataframe(df_prices.head(20))
    else:
        st.warning("Пожалуйста, загрузите и ТЗ, и хотя бы один прайс.")

