# DDS-group-17
# Career Mongo: : A personalized Job Search Engine

## Overview
Career Mongo is a project aimed at helping users find relevant job opportunities based on their skills and work experience. It utilizes various technologies such as web scraping, natural language processing, and database management to provide job recommendations and streamline the job search process.

## Files

### 1. DAG_Airflow.py
This file defines an Airflow DAG (Directed Acyclic Graph) named `upsert_jobs_daily`. It contains a task (`task1`) that is responsible for scraping job listings from multiple job search websites, generating embeddings for the job descriptions, and storing the data in a MongoDB database.

### 2. backend.py
The `backend.py` file contains the backend logic for interacting with the MongoDB database. It includes a `MongoDBConnection` class that handles database connections and provides a method for searching job listings based on user queries. Additionally, it includes a function `summarize_experience` for summarizing the work experience from a given resume text.

### 3. app.py
The `app.py` file is the main application file that implements a Streamlit web application. It allows users to input their job preferences or upload a resume, and then displays relevant job recommendations based on the input. The application interacts with the MongoDB database using the methods defined in `backend.py`.

### 4. models.py
The `models.py` file contains the definition of the models used in the project. It includes the following classes:

- `Model`: A base class for all models.
- `TextModel`: A subclass of `Model` that represents a text completion model. It utilizes OpenAI's GPT (Generative Pre-trained Transformer) model to generate text completions based on a given prompt.
- `generate_embedding`: A function that generates embeddings for text using OpenAI's text embedding model.

## Methodology

1. **Data Scraping from Job Posting Sites:** Job postings are gathered from popular platforms including Indeed, LinkedIn, ZipRecruiter, and Glassdoor using the jobspy library. This ensures a comprehensive dataset representing a wide range of job opportunities.

2. **Creation of a Dataframe and Embeddings:** Upon collecting the job descriptions, the text is transformed into embeddings using OpenAI. Each job description is represented as a numerical vector, allowing for efficient comparison and matching with user resumes.

3. **Employment of MongoDB for Data Storage:** The compiled dataframe containing job descriptions and embeddings is transferred to a MongoDB Atlas vector store. MongoDB's flexibility and scalability make it an ideal choice for storing large and complex datasets.

4. **Resume Tokenization and Embedding:** For the user-end of the system, resumes are tokenized and summarized using GPT models for summarization and OpenAI's text-embedding model for embedding generation. This ensures that user resumes are represented in a format compatible with job description embeddings.

5. **Matching Algorithm: K-Nearest Neighbor:** The core of the search engine is the K-nearest neighbor algorithm, which matches job seekers with jobs based on the similarity of their respective embeddings. By comparing the embeddings of user resumes with job description embeddings, the algorithm identifies the most relevant job postings for each user.

6. **Automated Updating with Airflow:** To ensure that the database remains current, Airflow is integrated to automate the updating process. The system is scheduled to refresh job postings daily, maintaining the relevance and accuracy of job recommendations.

7. **Streamlit for User Interface:** An intuitive user interface is developed using Streamlit, allowing users to upload their resumes and immediately view the most relevant job postings based on the matching algorithm. The interface provides a seamless and interactive experience for job seekers.

## Requirements
- pandas
- pymongo
- openai
- airflow
- streamlit
- llama_parse
- dotenv

## Usage
To run the application, follow these steps:
1. Run the Airflow DAG to scrape job listings and store them in the MongoDB database.
2. Execute the Streamlit application (`streamlit run app.py`) to launch the web interface.
3. Enter your job preferences or upload a resume to receive personalized job recommendations.

