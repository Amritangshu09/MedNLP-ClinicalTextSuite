"""
train_ner.py
Clinical NER with automatic fallback.
Public helpers:
    • extract_entities(text) -> List[Dict]
    • extract_drug_names(text) -> List[str]
"""

from typing import List, Dict

# ──────────────────────────────────────────────────────────────────────────────
# 1️⃣  PRIMARY BACKEND → SciSpacy (en_ner_bc5cdr_md)
# ──────────────────────────────────────────────────────────────────────────────
try:
    import spacy

    _nlp = spacy.load("en_ner_bc5cdr_md")  # ensure model installed

    def extract_entities(text: str) -> List[Dict]:
        doc = _nlp(text)
        return [{"entity": ent.label_, "word": ent.text} for ent in doc.ents]

    def extract_drug_names(text: str) -> List[str]:
        ents = extract_entities(text)

        phrases, current = [], []
        for ent in ents:
            tag = ent["entity"].lower()
            word = ent["word"]
            if tag not in {"chemical", "drug", "medication", "treatment"}:
                if current:
                    phrases.append(current)
                    current = []
                continue
            current.append(word)
        if current:
            phrases.append(current)

        return list({ " ".join(p).lower() for p in phrases if p })

    print("✅ NER backend: SciSpacy en_ner_bc5cdr_md")

# ──────────────────────────────────────────────────────────────────────────────
# 2️⃣  FALLBACK BACKEND → Hugging‑Face (d4data/biomedical-ner-all)
# ──────────────────────────────────────────────────────────────────────────────
except Exception as e:
    print("⚠️ SciSpacy unavailable – switching to Hugging Face backend.")
    print("ℹ️ Reason:", e)

    from transformers import pipeline

    # grouped_entities=False so we receive sub‑tokens & offsets
    _hf = pipeline(
        "ner",
        model="d4data/biomedical-ner-all",
        grouped_entities=False,
        device_map="auto",
    )

    def extract_entities(text: str) -> List[Dict]:
        raw = _hf(text)
        # keep start / end for later grouping
        return [
            {
                "entity": r["entity_group"] if "entity_group" in r else r["entity"],
                "word": r["word"],
                "start": r["start"],
                "end": r["end"],
            }
            for r in raw
        ]

    def extract_drug_names(text: str) -> List[str]:
        ents = sorted(extract_entities(text), key=lambda x: x["start"])
        phrases, current = [], []
        last_end = -1
        for ent in ents:
            tag = ent["entity"].lower()
            word = ent["word"].lstrip("#")  # remove leading ##
            if tag not in {"chemical", "drug", "medication", "treatment"}:
                if current:
                    phrases.append(current)
                    current = []
                continue

            # if contiguous token (no gap) → same phrase
            if current and ent["start"] <= last_end + 1:
                current.append(word)
            else:
                if current:
                    phrases.append(current)
                current = [word]
            last_end = ent["end"]

        if current:
            phrases.append(current)

        return list({ " ".join(p).lower() for p in phrases if p })

    print("✅ NER backend: Hugging Face d4data/biomedical-ner-all")

# ──────────────────────────────────────────────────────────────────────────────
# CLI quick‑test
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = (
        "The patient was prescribed Amoxicillin for infection and is on "
        "Methotrexate. Ibuprofen was taken along with Aspirin; Warfarin was stopped."
    )
    print("\nEntities ↓")
    for e in extract_entities(sample):
        print(e)
    print("\nDrugs ↓", extract_drug_names(sample))
