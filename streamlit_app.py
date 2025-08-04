import streamlit as st
from openai import OpenAI
import PyPDF2  # Add this for PDF parsing
import io

st.title("📄 Document Question Answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Get OpenAI API Key
# openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = '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'
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, .pdf)", type=("txt", "md", "pdf")
    )

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        file_text = ""
        file_type = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_type in ["txt", "md"]:
                file_text = uploaded_file.read().decode("utf-8")
            elif file_type == "pdf":
                # Read PDF using PyPDF2
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                for page in pdf_reader.pages:
                    file_text += page.extract_text() or ""
            else:
                st.error("Unsupported file type.")
        except Exception as e:
            st.error(f"Failed to read the file: {e}")

        if file_text:
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {file_text} \n\n---\n\n {question}",
                }
            ]

            try:
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    stream=True,
                )
                st.write_stream(stream)
            except Exception as e:
                st.error(f"Failed to generate answer: {e}")
