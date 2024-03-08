from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from jobspy import scrape_jobs
from pymongo import MongoClient
from models import *


def upsert_jobs():

    def scrape_and_create_embeddings(site_name):
        jobs = scrape_jobs(site_name=site_name)
        
        embeddings = []
        for index, row in jobs.iterrows():
            description = row['description']
            #print(description)  # Accessing description column
            if description == None:
                embeddings.append(description)
            else:
                embedding = generate_embedding(description)
                embeddings.append(embedding)

        # Add the embeddings list as a new column named 'embedding' to the DataFrame
        jobs['embedding'] = embeddings
        jobs['date_posted'] = jobs['date_posted'].astype(str)

        return jobs

    jobs = scrape_and_create_embeddings(
        site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"])
    # Connect to your MongoDB Atlas cluster
    uri = "mongodb+srv://john:SL1LnpJbWPWfB6Qb@cluster0.mayl8we.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["DistributedSystems"]
    collection = db["Project"]

    # Add the embeddings list as a new column named 'embedding' to the DataFrame
    for index, row in jobs.iterrows():
        # Convert the row to a dictionary and insert it into the MongoDB collection
        collection.insert_one(row.to_dict())

    return


with DAG(
    dag_id='upsert_jobs_daily',
    start_date=datetime(2024, 3, 9),
    schedule='0 1 * * *'
) as dag:
    task1 = PythonOperator(
        task_id='task1',
        python_callable=upsert_jobs)
