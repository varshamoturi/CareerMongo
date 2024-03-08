from models import *
import pandas as pd
import os
import pymongo


class MongoDBConnection:
    def __init__(self):
        self.user = os.getenv("USER_NAME")
        self.password = os.getenv("MONGODB_PASSWORD")
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{self.user}:{self.password}@cluster0.mayl8we.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client.DistributedSystems
        self.collection = self.db.SearchEngineProject

    def search(self, query):
        results = self.collection.aggregate([
            {"$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "embedding",
                "numCandidates": 100,
                "limit": 8,
                "index": "OpenaiSemanticSearch",
            }}
        ])

        data = [{'title': doc['title'], 'company': doc['company'], 'date posted': doc['date_posted'], 'job url': doc['job_url']}
                for doc in results]
        df = pd.DataFrame(
            data, columns=['title', 'company', 'date posted', 'job url'])
        return df


def summarize_experience(resume_text):
    prompt = f"Please summarize the following resume in three sentences, focusing on the person's skills and work experience: \n\n{resume_text}"
    text_model = TextModel()
    summary = text_model.complete(prompt)
    return summary
