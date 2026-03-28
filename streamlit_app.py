import streamlit as st
import pandas as pd
from service import process_single, process_batch

st.set_page_config(page_title="Sentiment Analyzer", layout="wide")
st.title("Sentiment Analysis Dashboard")

st.sidebar.header("Настройки")
mode = st.sidebar.selectbox("Выберете мод", ["Single text", "Batch (multiple texts)"])


if "history" not in st.session_state:
    st.session_state.history = []


if mode == "Single text":
    st.subheader("Analyze single text")
    text = st.text_area("Enter text", height=150)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Проверить"):
            result = process_single(text)
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.history.append(result)
                st.success("Анализ завершен!")
                st.json(result)

    with col2:
        if st.button("Очистить историю"):
            st.session_state.history = []


else:
    st.subheader("Batch analysis")
    texts = st.text_area(
        "Введите несколько текстов (по одному на строку).",
        height=200
    )

    if st.button("Analyze batch"):
        results = process_batch(texts)
        if results:
            st.session_state.history.extend(results)
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.warning("Нет действительных текстов")


st.subheader("История")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    st.subheader("Statistics")
    st.bar_chart(df["label"].value_counts())
else:
    st.info("История пока отсутствует")