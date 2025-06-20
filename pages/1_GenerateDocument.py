
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Generate Document", layout="wide")
st.title("🧠 Document Generator")

if "documents" not in st.session_state:
    st.warning("Please upload files on the home page first.")
    st.stop()

# Concatenate all documents
all_docs = "\n\n".join(st.session_state["documents"])

# Configure Gemini
genai.configure(api_key=st.secrets["gemini_api_key"])

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

st.subheader("Choose a Template")

template = st.radio(
    "Select a document generation template:",
    options=["📄 Summary Report", "📊 Actionable Insights"]
)

if template == "📄 Summary Report":
    prompt = f"Summarize the following multi-format documents (text, CSV, Excel) into a clear and structured report:\n\n{all_docs}"
elif template == "📊 Actionable Insights":
    prompt = f"Analyze the following mixed-format documents and extract meaningful insights and action items:\n\n{all_docs}"

if st.button("📄 Generate Document"):
    with st.spinner("Generating document..."):
        try:
            response = model.generate_content(prompt)
            generated = response.text
            st.session_state["generated_doc"] = generated
            st.success("Document generated successfully!")
        except Exception as e:
            st.error(f"🚨 An error occurred while calling Gemini: {str(e)}")

# Preview & Download
if "generated_doc" in st.session_state:
    st.subheader("📑 Preview of Generated Document")
    st.text_area("Generated Output", value=st.session_state["generated_doc"], height=400)

    st.download_button("💾 Download as .txt", st.session_state["generated_doc"], file_name="generated_document.txt")
