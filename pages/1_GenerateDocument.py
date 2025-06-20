import streamlit as st
import openai

st.set_page_config(page_title="Document Generator", page_icon="🧠")

st.sidebar.title("Home")
st.sidebar.markdown("## GenerateDocument")

st.title("🧠 Document Generator")

# Template selection
template = st.radio(
    "Select a document generation template:",
    ("Summary Report", "Actionable Insights"),
)

# User input
prompt = st.text_area("Enter text to generate a document:", height=200)

if st.button("Generate Document"):
    if not prompt.strip():
        st.warning("⚠️ Please enter some text to proceed.")
    else:
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            model = "gpt-4"
            fallback_model = "gpt-3.5-turbo"

            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": f"You are generating a {template.lower()}."},
                        {"role": "user", "content": prompt},
                    ],
                )
            except openai.error.InvalidRequestError as e:
                if "model" in str(e) and "not found" in str(e):
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

            generated_text = response.choices[0].message["content"].strip()
            st.success(f"✅ Document generated with **{model}**")
            st.text_area("Generated Document:", value=generated_text, height=300)

        except openai.error.AuthenticationError:
            st.error("❌ Authentication failed. Check your OpenAI API key.")
        except openai.error.OpenAIError as e:
            st.error(f"❌ OpenAI error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

