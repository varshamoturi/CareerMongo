import streamlit as st
import pandas as pd
import PyPDF2
from jobspy import scrape_jobs

st.title("Find jobs")

### Upload PDF
# File uploader component
uploaded_file = st.file_uploader("Upload your resume as PDF file", type=["pdf"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read PDF file contents
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    # Display PDF content
    st.write("### PDF Content:")
    st.write(text)


### Dispayling Sample jobs form jobs.py
company_name = st.text_input("Enter the name of the company:")
if company_name== '':
    company_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"]


jobs = scrape_jobs(
    site_name = company_name,  
    #["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    search_term="data Science",
    location="Dallas, TX",
    results_wanted=20,
    hours_old=72, # (only linkedin is hour specific, others round up to days old)
    country_indeed='USA'  # only needed for indeed / glassdoor
)
print(f"Found {len(jobs)} jobs")
# Convert JSON to DataFrame
sample_display=jobs[["company","title","job_url"]]
# Display DataFrame as a table
col1, col2, col3 = st.columns([1, 2,3])
st.dataframe(sample_display,column_config={
        "company": "Company name",
        "title":"Job title",
        "job_url": st.column_config.LinkColumn("App URL"),
        # "views_history": st.column_config.LineChartColumn(
        #     "Views (past 30 days)", y_min=0, y_max=5000
        # ),
    },
    hide_index=True, width=20000, height=400)
# st.write("### JSON Data as Table")
# st.write(df)