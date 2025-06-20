import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Generate Document", layout="wide")

st.title("🧠 Document Generator")

if "documents" not in st.session_state:
    st.warning("Please upload files on the home page first.")
    st.stop()

# Concatenate all documents
all_docs = "\n\n".join(st.session_state["documents"])

# Access OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.subheader("Choose a Template")

template = st.radio(
    "Select a document generation template:",
    options=["📄 Summary Report", "📊 Actionable Insights"]
)

prompt = ""
if template == "📄 Summary Report":
    prompt = f"Summarize the following documents into a well-structured report:\n\n{all_docs}"
elif template == "📊 Actionable Insights":
    prompt = f"Analyze the following documents and extract key insights and action items:\n\n{all_docs}"

if st.button("📄 Generate Document"):
    with st.spinner("Generating document..."):
        response = client.chat.completions.create(
            model="gpt-4",  # Change to gpt-3.5-turbo if needed
            messages=[{"role": "user", "content": prompt}],
        )
        generated = response.choices[0].message.content
        st.session_state["generated_doc"] = generated
        st.success("Document generated successfully!")

if "generated_doc" in st.session_state:
    st.subheader("📑 Preview of Generated Document")
    st.text_area("Generated Output", value=st.session_state["generated_doc"], height=400)

    st.download_button("💾 Download as .txt", st.session_state["generated_doc"], file_name="generated_document.txt")
