import streamlit as st
import openai
import os
import tempfile

from docx import Document
from PyPDF2 import PdfReader

# Set up Streamlit page
st.set_page_config(page_title="Document Editor", page_icon="📝")

st.title("📝 AI-Powered Document Editor")
st.markdown("Upload a document and describe how you’d like to modify it.")

# File uploader
uploaded_file = st.file_uploader("Upload a .txt, .docx or .pdf file", type=["txt", "docx", "pdf"])

# Edit prompt
edit_prompt = st.text_area("Enter what you want to change or add:", height=150)

# OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text(file):
    file_type = file.name.split(".")[-1].lower()
    if file_type == "txt":
        return file.read().decode("utf-8")
    elif file_type == "docx":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_type == "pdf":
        reader = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        return ""

def generate_new_document(content, instructions):
    prompt = (
        "You are a document editor. Based on the following original content, "
        "apply the user's instructions to improve or modify the document.\n\n"
        "Instructions:\n"
        f"{instructions}\n\n"
        "Original Document:\n"
        f"{content}\n\n"
        "Edited Document:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Fallback logic can be added here
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

if st.button("Generate Edited Document"):
    if not uploaded_file or not edit_prompt.strip():
        st.warning("Please upload a document and provide editing instructions.")
    else:
        with st.spinner("Generating document..."):
            try:
                original_text = extract_text(uploaded_file)
                updated_text = generate_new_document(original_text, edit_prompt)

                st.success("✅ Document generated successfully.")
                st.text_area("Preview:", value=updated_text, height=300)

                # Prepare download
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
                tmp.write(updated_text.encode("utf-8"))
                tmp.close()

                with open(tmp.name, "rb") as f:
                    st.download_button(
                        label="📥 Download Edited Document",
                        data=f,
                        file_name="edited_document.txt",
                        mime="text/plain"
                    )

                os.unlink(tmp.name)
            except Exception as e:
                st.error(f"An error occurred: {e}")
