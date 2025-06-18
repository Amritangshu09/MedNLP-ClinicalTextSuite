import streamlit as st
import sys
import os

# 🔧 Fix Python path to allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.mednlp.ner.train_ner import extract_entities, extract_drug_names
from src.mednlp.drug_interaction.interaction_detector import check_interactions

# --- Page Configuration ---
st.set_page_config(page_title="Clinical NLP Suite", layout="wide")

# --- Sidebar ---
st.sidebar.markdown("## 🛠️ Choose a Task")
selected_module = st.sidebar.radio("Select Module", [
    "Named Entity Recognition",
    "Note Summarization",
    "Drug Interaction Checker"
])

# --- App Header ---
st.markdown("<h1 style='font-size: 3em;'>Suite</h1>", unsafe_allow_html=True)
st.markdown("Built with ❤️ for clinical text processing")

# --- Named Entity Recognition Module ---
if selected_module == "Named Entity Recognition":
    st.subheader("🔎 Named Entity Recognition (NER)")
    clinical_text = st.text_area("Enter clinical text here:")

    if st.button("Run NER"):
        if clinical_text.strip():
            with st.spinner("Processing..."):
                try:
                    entities = extract_entities(clinical_text)
                    st.success("Entities found:")
                    st.json(entities)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("Please enter some clinical text.")

# --- Drug Interaction Checker Module ---
# elif selected_module == "Drug Interaction Checker":
#     st.subheader("💊 Drug Interaction Checker")
#     user_input = st.text_input("Enter drugs (comma-separated):", 
#                                placeholder="e.g., The patient was prescribed Amoxicillin and Methotrexate.")

#     if st.button("Check Interactions"):
#         if user_input.strip():
#             with st.spinner("🔍 Extracting drug names using NER..."):
#                 try:
#                     # Step 1: Extract entities using NER
#                     entities = extract_entities(user_input)

#                     # Step 2: Filter only drug entities
#                     drug_names = [e["word"] for e in entities if "drug" in e["entity"].lower()]

#                     # Step 3: Display extracted drugs
#                     if drug_names:
#                         st.markdown("🧪 **Detected drug(s):** " + " | ".join([f"**`{d}`**" for d in drug_names]))
#                     else:
#                         st.warning("⚠️ No drug names detected. Try again with clearer input.")
#                         st.stop()

#                     # Step 4: Check for interactions
#                     interactions = check_interactions(drug_names)

#                     if interactions:
#                         for item in interactions:
#                             drug1, drug2 = item['drug_pair']
#                             st.warning(f"⚠️ Interaction detected between **{drug1}** and **{drug2}**")
#                             st.info(f"💡 Caution: {item['info']}")
#                     else:
#                         st.success("✅ No known interactions detected.")
                
#                 except Exception as e:
#                     st.error(f"❌ Error: {str(e)}")
#         else:
#             st.error("Please enter a sentence containing drug names.")

# # --- Note Summarization Module (Placeholder) ---
# elif selected_module == "Note Summarization":
#     st.subheader("📝 Note Summarization")
#     st.info("🚧 This module is under development. Stay tuned!")

# --- Drug Interaction Checker Module ---
elif selected_module == "Drug Interaction Checker":
    st.subheader("💊 Drug Interaction Checker")
    user_input = st.text_area("Enter clinical text containing drug names:", 
                           placeholder="e.g., The patient was prescribed Amoxicillin and Methotrexate.")

    if st.button("Check Interactions"):
        if user_input.strip():
            with st.spinner("🔍 Analyzing..."):
                try:
                    # Extract drug names
                    drug_names = extract_drug_names(user_input)
                    st.markdown("🧪 **Drugs detected after cleaning:**")
                    st.code(", ".join(drug_names))

                    
                    if not drug_names:
                        st.warning("⚠️ No drug names detected. Try different text.")
                        st.stop()
                    
                    st.markdown("🧪 **Detected drug(s):** " + ", ".join([f"`{d}`" for d in drug_names]))
                    
                    # Check interactions
                    interactions = check_interactions(drug_names)
                    
                    if interactions:
                        for item in interactions:
                            drug1, drug2 = item['drug_pair']
                            st.warning(f"🚨 **{drug1} + {drug2}** → {item['info']}")
                            st.info(f"💡 {item['info']}")
                    else:
                        st.success("✅ No known interactions between these drugs.")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.error("Please enter some text containing drug names.")


# --- Note Summarization Module ---
elif selected_module == "Note Summarization":
    from src.mednlp.summarization.summarizer import summarize_note
    from src.mednlp.ner.train_ner import extract_entities
    from fpdf import FPDF
    import streamlit.components.v1 as components
    import re, uuid, os

    st.subheader("📝 Note Summarization")

    # ── Input and options ──────────────────────────────────────────────────────
    input_note = st.text_area("Paste clinical note here:", height=220)

    col1, col2 = st.columns(2)
    with col1:
        max_len = st.slider("🪄 Max length", 50, 300, 120, 10)
    with col2:
        min_len = st.slider("✨ Min length", 20, max_len - 10, 30, 5)

    # ── Summarize button ───────────────────────────────────────────────────────
    if st.button("Summarize Note"):
        if not input_note.strip():
            st.warning("Please enter some clinical text.")
            st.stop()

        with st.spinner("🧠 Summarizing..."):
            try:
                summary = summarize_note(input_note, max_len, min_len)  # <-- we’ll tweak summarizer.py to accept len
            except TypeError:
                # if summarize_note had fixed params, fall back
                summary = summarize_note(input_note)

        # ── Show raw summary ───────────────────────────────────────────────────
        st.success("📝 **Summary:**")
        st.write(summary)

        # ── Highlight clinical terms inside summary ───────────────────────────
        entities = extract_entities(summary)
        highlighted = summary
        # replace longest words first to avoid nested replacements
        for ent in sorted(entities, key=lambda x: -len(x["word"])):
            # simple word‑boundary regex to avoid mid‑word replacement
            pattern = r"\b" + re.escape(ent["word"]) + r"\b"
            repl = f"**🧠 _{ent['word']}_**"
            highlighted = re.sub(pattern, repl, highlighted, flags=re.IGNORECASE)

        st.markdown("🧬 **Summary with Clinical Highlights:**")
        st.markdown(highlighted)

        # ── Export options ─────────────────────────────────────────────────────
        ## 1.  Download as PDF
        import tempfile

        def make_pdf(text: str) -> str:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            for line in text.split("\n"):
                pdf.multi_cell(0, 8, line)

            # Save to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(temp_file.name)
            return temp_file.name


        pdf_path = make_pdf(summary)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download summary as PDF", f, "summary.pdf", "application/pdf")

        ## 2.  Copy to clipboard (JS)
        components.html(
            f"""
            <textarea id="clip" style="width:100%;height:0;">{summary}</textarea>
            <button style="margin-top:10px;padding:6px 14px;border-radius:6px;"
                    onclick="navigator.clipboard.writeText(document.getElementById('clip').value)">
              📋 Copy summary to clipboard
            </button>
            """,
            height=60,
        )
