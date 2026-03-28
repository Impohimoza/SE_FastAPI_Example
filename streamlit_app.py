import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

st.title("📊 Sentiment Analysis Dashboard")

st.sidebar.header("⚙️ Настройки")
mode = st.sidebar.selectbox("Выберете мод", ["Single text", "Batch (multiple texts)"])

if "history" not in st.session_state:
    st.session_state.history = []

if mode == "Single text":
    st.subheader("🔍 Analyze single text")

    text = st.text_area("Enter text", height=150)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Проверить"):
            if text.strip():
                response = requests.post(
                    f"{API_URL}/predict/",
                    json={"text": text}
                )
                result = response.json()

                st.session_state.history.append({
                    "text": text,
                    "label": result[0]["label"],
                    "score": result[0]["score"]
                })

                st.success("Анализ завершен!")
                st.json(result)
            else:
                st.error("Текст пуст")

    with col2:
        if st.button("Очистить историю"):
            st.session_state.history = []

else:
    st.subheader("📂 Batch analysis")

    texts = st.text_area(
        "Введите несколько текстов (по одному на строку).",
        height=200
    )

    if st.button("Analyze batch"):
        results = []
        for t in texts.split("\n"):
            if t.strip():
                response = requests.post(
                    f"{API_URL}/predict/",
                    json={"text": t}
                )
                result = response.json()[0]

                results.append({
                    "text": t,
                    "label": result["label"],
                    "score": result["score"]
                })

                st.session_state.history.append(results[-1])

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
        else:
            st.warning("Нет действительных текстов")

st.subheader("🕓 История")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    st.subheader("📈 Statistics")
    st.bar_chart(df["label"].value_counts())
else:
    st.info("История пока отсутствует")
