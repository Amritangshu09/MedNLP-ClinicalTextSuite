from transformers import pipeline

# Load summarization pipeline once
summarizer = pipeline("summarization", model="Falconsai/text_summarization")


def summarize_note(text: str, max_len: int = 120, min_len: int = 30) -> str:
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]["summary_text"]

