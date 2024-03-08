from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()


class Model:
    def __init__(self, model_name):
        self.model_name = model_name


class TextModel(Model):
    def __init__(self, model_name="gpt-4-1106-preview"):
        super().__init__(model_name)

    def complete(self, prompt, role="You are an experienced recruiter"):
        messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": prompt}
        ]

        completion = client.chat.completions.create(model=self.model_name,
                                                    temperature=0,
                                                    messages=messages)
        return completion.choices[0].message.content


def generate_embedding(text, model="text-embedding-3-small"):
    client = OpenAI()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
