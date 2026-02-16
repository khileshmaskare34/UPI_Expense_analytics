import re
import string

def clean_text(text: str) -> str:
    """Lowercase and clean UPI description text."""
    text = text.lower()
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    text = text.strip()
    return text
