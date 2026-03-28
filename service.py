from api_client import analyze_text

def process_single(text: str):
    """
    Обработка одиночного текста.
    """
    if not text.strip():
        return {"error": "Empty text"}
    result = analyze_text(text)[0]
    return {
        "text": text,
        "label": result["label"],
        "score": result["score"]
    }

def process_batch(texts: str):
    """
    Обработка нескольких текстов (по одному на строку).
    """
    results = []
    for t in texts.split("\n"):
        if t.strip():
            result = analyze_text(t)[0]
            results.append({
                "text": t,
                "label": result["label"],
                "score": result["score"]
            })
    return results