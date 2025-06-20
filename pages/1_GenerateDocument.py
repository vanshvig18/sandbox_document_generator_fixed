import streamlit as st
import openai

# Streamlit config
st.set_page_config(page_title="Document Generator", page_icon="🧠")

# Sidebar
st.sidebar.title("Home")
st.sidebar.markdown("## GenerateDocument")

# Main title
st.title("🧠 Document Generator")

# Template selector
template = st.radio(
    "Select a document generation template:",
    ("Summary Report", "Actionable Insights"),
)

# Prompt input
prompt = st.text_area("Enter text to generate a document:", height=200)

# Generate button
if st.button("Generate Document"):
    if not prompt.strip():
        st.warning("⚠️ Please enter some text to proceed.")
    else:
        try:
            # Set API key
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            model = "gpt-4"
            fallback_model = "gpt-3.5-turbo"

            try:
                # Try GPT-4
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are generating a {template.lower()}."},
                        {"role": "user", "content": prompt},
                    ],
                )
            except openai.error.InvalidRequestError as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    # Fallback to GPT-3.5
                    model = fallback_model
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": f"You are generating a {template.lower()}."},
                            {"role": "user", "content": prompt},
                        ],
                    )
                else:
                    raise

            # Extract and display result
            generated_text = response.choices[0].message["content"].strip()
            st.success(f"✅ Document generated with **{model}**")
            st.text_area("Generated Document:", value=generated_text, height=300)

        except openai.error.OpenAIError as e:
            if "authentication" in str(e).lower():
                st.error("❌ Authentication failed. Check your OpenAI API key.")
            else:
                st.error(f"❌ OpenAI error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
