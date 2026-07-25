import json
import streamlit as st
import google.generativeai as genai
from PIL import Image


def analyze_expense_with_ai(api_key: str, text_input: str = None, image_input: Image.Image = None) -> dict:
    clean_key = api_key.strip()
    genai.configure(api_key=clean_key)

    # Priority list of current active Gemini Flash models
    candidate_models = [
        'gemini-3.6-flash',
        'gemini-3.5-flash',
        'gemini-3.5-flash-lite',
        'gemini-3-flash'
    ]

    prompt = """
    Extract expense details from the input.
    Return strictly a raw JSON object with NO markdown wrapping or backticks:
    {
        "item": "description string",
        "amount": 0.00,
        "category": "Food"
    }
    Categories must be one of: "Food", "Transport", "Shopping", "Bills", "Entertainment", "Other".
    """

    contents = [prompt]
    if image_input:
        contents.append(image_input)
    if text_input:
        contents.append(f"Expense text: {text_input}")

    response = None
    last_error = None

    # Try active models in sequence until one succeeds
    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            if response and response.text:
                break
        except Exception as err:
            last_error = err
            continue

    if not response or not response.text:
        st.error(f"API Error Details: {last_error}")
        raise Exception(f"Failed to fetch response. Last error: {last_error}")

    cleaned = response.text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    return json.loads(cleaned)
