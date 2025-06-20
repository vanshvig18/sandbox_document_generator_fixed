import streamlit as st
import pandas as pd

st.set_page_config(page_title="Multi-Doc QA & Generator", layout="wide")

st.title("📁Sandbox based Document Generator")
st.write("Upload `.txt`, `.csv`, or `.xlsx` files to generate a custom document using templates.")

uploaded_files = st.file_uploader(
    "Upload files (TXT, CSV, XLSX):",
    type=["txt", "csv", "xlsx"],
    accept_multiple_files=True,
)

# Read all files and save text content
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode()
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.to_string(index=False)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.to_string(index=False)
    else:
        return ""

if uploaded_files:
    contents = [extract_text(f) for f in uploaded_files]
    st.session_state["documents"] = contents
    st.success(f"{len(uploaded_files)} files uploaded successfully!")

    if st.button("➡ Proceed to Generate Document"):
        st.success("Now go to the sidebar and select 'Generate Document' to continue.")
