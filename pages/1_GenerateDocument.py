import streamlit as st
from openai import OpenAI, error as OpenAIError

# App configuration
st.set_page_config(page_title="Document Generator", page_icon="🧠")

# Sidebar
st.sidebar.title("Home")
st.sidebar.markdown("## GenerateDocument")

# Title
st.title("🧠 Document Generator")

# Template selection
template = st.radio(
    "Select a document generation template:",
    ("Summary Report", "Actionable Insights"),
)

# User input
prompt = st.text_area("Enter text to generate a document:", height=200)

# Action button
if st.button("Generate Document"):
    if not prompt.strip():
        st.warning("⚠️ Please enter some text to proceed.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            model = "gpt-4"
            fallback_model = "gpt-3.5-turbo"

            try:
                # Try GPT-4
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are generating a {template.lower()}."},
                        {"role": "user", "content": prompt},
                    ],
                )
            except OpenAIError.InvalidRequestError as e:
                if "model" in str(e) and "not found" in str(e):
                    model = fallback_model  # Fallback
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": f"You are generating a {template.lower()}."},
                            {"role": "user", "content": prompt},
                        ],
                    )
                else:
                    raise

            # Display response
            generated_text = response.choices[0].message.content.strip()
            st.success(f"✅ Document generated with **{model}**")
            st.text_area("Generated Document:", value=generated_text, height=300)

        except OpenAIError.AuthenticationError:
            st.error("❌ Authentication failed. Check your OpenAI API key in the app settings.")
        except OpenAIError.OpenAIError as e:
            st.error(f"❌ OpenAI error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
