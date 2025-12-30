from crewai import LLM
import os
from tools.token_counter import track_token_usage, estimate_tokens_for_model


# --------------------------------------------------
# Utility: ensure required env vars exist
# --------------------------------------------------
def _require_env(key: str):
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# --------------------------------------------------
# LIGHT LLM (Groq – small model)
# Used for: discovery, extraction
# --------------------------------------------------
def get_light_llm():
    _require_env("GROQ_API_KEY")
    
    model_name = os.getenv("OPEN_MODEL_NAME", "llama-3.1-8b-instant")

    return LLM(
        model=model_name,
        api_base="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),   # ✅ REAL KEY
        temperature=0.2
    )


# --------------------------------------------------
# MEDIUM LLM (Gemini – summarization / aggregation)
# --------------------------------------------------
def get_medium_llm():
    _require_env("GEMINI_API_KEY")
    
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")

    return LLM(
        model=model_name,
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    )


# --------------------------------------------------
# STRONG LLM (Groq – reasoning / strategy)
# --------------------------------------------------
def get_strong_llm():
    _require_env("GROQ_API_KEY")
    
    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")

    return LLM(
        model=model_name,
        api_base="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),   # ✅ REAL KEY
        temperature=0.4
    )
