def detect_language(text):
    for char in text:
        if '\u0900' <= char <= '\u097F':
            return "hi"
    return "en"

