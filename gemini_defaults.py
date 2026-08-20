import os

def default_gemini_model(model=None):
    return model or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
