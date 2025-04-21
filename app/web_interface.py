import streamlit as st

st.set_page_config(page_title="AI-сервис подбора", layout="wide")

st.title("🤖 AI-сервис подбора оборудования")
st.markdown("Загрузите техническое задание и прайс-листы — система всё сделает сама.")

# Блок загрузки ТЗ
st.header("📄 Техническое задание")
uploaded_spec = st.file_uploader("Загрузите файл с ТЗ (PDF, DOCX)", type=["pdf", "docx"])

# Блок загрузки прайсов
st.header("📊 Прайсы поставщиков")
uploaded_prices = st.file_uploader("Загрузите 1 или несколько прайсов (Excel)", type=["xlsx"], accept_multiple_files=True)

# Кнопка запуска анализа
if st.button("🚀 Запустить подбор"):
    if uploaded_spec and uploaded_prices:
        st.success("Файлы получены! Идёт обработка...")
        # тут будет подключение backend логики
    else:
        st.warning("Пожалуйста, загрузите и ТЗ, и хотя бы один прайс.")

