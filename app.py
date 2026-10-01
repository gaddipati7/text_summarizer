import streamlit as st
import os
from dotenv import load_dotenv
from mistralai.client import Mistral

# ==========================================
# 1. Load API Key
# ==========================================

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")

# ==========================================
# 2. Page Configuration
# ==========================================

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# ==========================================
# 3. Application Title
# ==========================================

st.title("📝 AI Text Summarizer")

st.write(
    "Enter any text and generate a clear and concise summary."
)

st.divider()

# ==========================================
# 4. Check API Key
# ==========================================

if not API_KEY:
    st.error(
        "API key not found. Please check your .env file."
    )
    st.stop()

# ==========================================
# 5. Create Mistral Client
# ==========================================

client = Mistral(
    api_key=API_KEY
)

# ==========================================
# 6. Text Input
# ==========================================

text = st.text_area(
    "Enter your text",
    height=300,
    placeholder="Paste your article, notes, paragraph, or document text here..."
)

# ==========================================
# 7. Summary Options
# ==========================================

col1, col2 = st.columns(2)

with col1:

    summary_length = st.selectbox(
        "Summary Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

with col2:

    language = st.selectbox(
        "Summary Language",
        [
            "English",
            "Telugu",
            "Hindi"
        ]
    )

# ==========================================
# 8. Generate Summary
# ==========================================

if st.button(
    "✨ Generate Summary",
    type="primary",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "Please enter some text before generating a summary."
        )

    else:

        # ----------------------------------
        # Select summary instruction
        # ----------------------------------

        if summary_length == "Short":

            instruction = """
Create a very short summary.
Include only the most important points.
"""

        elif summary_length == "Medium":

            instruction = """
Create a medium-length summary.
Include the main ideas and important supporting details.
"""

        else:

            instruction = """
Create a detailed summary.
Include the important ideas, supporting details,
key facts, and conclusions.
"""

        # ----------------------------------
        # Create Prompt
        # ----------------------------------

        prompt = f"""
You are an expert text summarization assistant.

Your task is to summarize the text provided by the user.

{instruction}

Additional requirements:

1. Write the summary in {language}.
2. Do not add information that is not present in the original text.
3. Preserve important facts, names, numbers, and conclusions.
4. Use clear and simple language.
5. Use bullet points when appropriate.

Original Text:

{text}
"""

        # ----------------------------------
        # Call Mistral API
        # ----------------------------------

        with st.spinner(
            "Generating summary..."
        ):

            try:

                response = client.chat.complete(
                    model="mistral-small-latest",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                # ----------------------------------
                # Extract response
                # ----------------------------------

                summary = (
                    response.choices[0]
                    .message
                    .content
                )

                # ----------------------------------
                # Display summary
                # ----------------------------------

                st.divider()

                st.subheader("📄 Generated Summary")

                st.write(summary)

                # ----------------------------------
                # Download summary
                # ----------------------------------

                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

# ==========================================
# 9. Footer
# ==========================================

st.divider()

st.caption(
    "Built using Python and Streamlit"
)