import streamlit as st
import fitz  # PyMuPDF
import docx2txt
import pandas as pd
import io
from rapidfuzz import fuzz

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

# Функция сопоставления позиций
def match_positions(spec_text, df_prices):
    results = []
    for line in spec_text.split("\n"):
        line = line.strip()
        if len(line) < 5:
            continue
        best_match = None
        best_score = 0
        for _, row in df_prices.iterrows():
            for col in df_prices.columns:
                if isinstance(row[col], str):
                    score = fuzz.token_sort_ratio(line.lower(), row[col].lower())
                    if score > best_score:
                        best_score = score
                        best_match = row
        if best_match is not None and best_score > 60:
            matched = best_match.to_dict()
            matched['Совпадение'] = best_score
            matched['Из ТЗ'] = line
            results.append(matched)
    return pd.DataFrame(results)

# Кнопка запуска анализа
if st.button("🚀 Запустить подбор"):
    if uploaded_spec and uploaded_prices:
        st.success("Файлы получены! Идёт обработка...")

        spec_text = extract_text_from_spec(uploaded_spec)
        st.subheader("📜 Распознанный текст из ТЗ")
        st.text_area("", spec_text, height=300)

        df_prices = read_prices(uploaded_prices)
        st.subheader("📋 Объединённый прайс-лист")
        st.dataframe(df_prices.astype(str).head(20))
        if not df_prices.empty and spec_text:
            df_result = match_positions(spec_text, df_prices)
            st.subheader("✅ Сопоставленные позиции")
            st.dataframe(df_result)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_result.to_excel(writer, index=False, sheet_name='Сопоставление')
            st.download_button("📥 Скачать результат в Excel", output.getvalue(), file_name="подбор_результат.xlsx")
    else:
        st.warning("Пожалуйста, загрузите и ТЗ, и хотя бы один прайс.")

