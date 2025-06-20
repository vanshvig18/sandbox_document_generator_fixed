import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError

st.set_page_config(page_title="Document Generator", page_icon="🧠")

st.sidebar.title("Home")
st.sidebar.markdown("## GenerateDocument")

st.title("🧠 Document Generator")

# Template selection
st.subheader("Choose a Template")
template = st.radio(
    "Select a document generation template:",
    ("Summary Report", "Actionable Insights"),
)

# Text area for input
prompt = st.text_area("Enter text to generate a document:", height=200)

# Generate button
if st.button("Generate Document"):
    if not prompt:
        st.warning("Please enter some text before generating the document.")
    else:
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are generating a {template.lower()}."},
                    {"role": "user", "content": prompt},
                ],
            )

            generated_text = response.choices[0].message.content
            st.success("✅ Document generated successfully!")
            st.text_area("Generated Document:", value=generated_text, height=300)

        except AuthenticationError:
            st.error("❌ Authentication failed. Please check your OpenAI API key in the app secrets.")
        except OpenAIError as e:
            st.error(f"❌ OpenAI API error: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
