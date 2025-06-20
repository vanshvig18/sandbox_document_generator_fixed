import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Generate Document", layout="wide")
st.title("🧠 Document Generator")

# Check if uploaded documents exist
if "documents" not in st.session_state:
    st.warning("Please upload files on the Home page first.")
    st.stop()

# Join all uploaded document content
all_docs = "\n\n".join(st.session_state["documents"])

# Check if OpenAI API key is available
if "openai_api_key" not in st.secrets:
    st.error("OpenAI API key is missing from Streamlit secrets. Please set it.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.subheader("Choose a Template")

template = st.radio(
    "Select a document generation template:",
    options=["📄 Summary Report", "📊 Actionable Insights"]
)

# Prepare the prompt based on selected template
if template == "📄 Summary Report":
    prompt = f"Summarize the following multi-format documents (text, CSV, Excel) into a clear and structured report:\n\n{all_docs}"
elif template == "📊 Actionable Insights":
    prompt = f"Analyze the following mixed-format documents and extract meaningful insights and action items:\n\n{all_docs}"

# Generate the document on button click
if st.button("📄 Generate Document"):
    with st.spinner("Generating document..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Fixed model
                messages=[{"role": "user", "content": prompt}],
            )
            generated = response.choices[0].message.content
            st.session_state["generated_doc"] = generated
            st.success("✅ Document generated successfully!")
        except Exception as e:
            st.error(f"❌ OpenAI API call failed: {e}")
            st.stop()

# Show document preview and download option
if "generated_doc" in st.session_state:
    st.subheader("📑 Preview of Generated Document")
    st.text_area("Generated Output", value=st.session_state["generated_doc"], height=400)
    
    st.download_button(
        "💾 Download as .txt",
        data=st.session_state["generated_doc"],
        file_name="generated_document.txt"
    )
