import streamlit as st
import pandas as pd
from llama_parse import LlamaParse
import os
from backend import MongoDBConnection, summarize_experience
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title='Career Mongo', layout='wide',
                   page_icon='icon.png', initial_sidebar_state='auto')
header_alignment_css = """
<style>
    th {
        text-align: left;
    }
</style>
"""

st.title("🛄 _Career Mongo_ ")
db_connection = MongoDBConnection()

# User query input
user_query = st.text_input("What job are you looking for?")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your resume as PDF file", type=["pdf"])

# Submit button
submit_button = st.button("Submit")

if submit_button:
    if uploaded_file:
        file_path = "temp_file.pdf"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        parser = LlamaParse(
            api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
            result_type="markdown",
            language="en"
        )
        document = parser.load_data(file_path)[0].text
        summary = summarize_experience(document)
        sub_title = "### Jobs that fit _your_ experience:"
    else:
        summary = user_query
        sub_title = "### Keyword based job recommendations"
    df = db_connection.search(summary)
    if not df.empty:
        st.write(sub_title)
        df['job url'] = df.apply(
            lambda row: f'<a href="{row["job url"]}">Link</a>', axis=1)
        df_html = header_alignment_css + df.to_html(escape=False, index=False)
        st.markdown(df_html, unsafe_allow_html=True)
    else:
        st.write("No results found based on the summary.")
