import openai
import numpy as np
from PyPDF2 import PdfReader
import pandas as pd
import json
from pymilvus import Collection, connections, utility, FieldSchema, DataType, CollectionSchema
import logging




def generate(question):
    
    # get API key
    openai.api_key = "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"
    embed_model = "text-embedding-ada-002"

    # logging file
    logging.basicConfig(filename="runtime.log", level=logging.DEBUG, format="{asctime}s %(levelname)s %(name)s %(threadName)s : %(message)s")


    # # text completion
    # def complete(prompt):
    #     # query text-davinci-003
    #     res = openai.Completion.create(
    #         engine='text-davinci-003',
    #         prompt=prompt,
    #         temperature=0,
    #         max_tokens=400,
    #         top_p=1,
    #         frequency_penalty=0,
    #         presence_penalty=0,
    #         stop=None
    #     )
    #     return res['choices'][0]['text'].strip()


    # transfrom pdf file into text
    def extractPDF(pdfFile):
        reader = PdfReader(pdfFile)
        pdfText = []
        for page in reader.pages:
            context = page.extract_text()
            pdfText.append(context)

        return pdfText


    text = extractPDF("./Resources/ruhnama.pdf")




    # define the embedding
    def embed(text):
        return openai.Embedding.create(
            input=text,
            engine=embed_model)["data"][0]["embedding"]




    logging.warning("1")
    connections.connect(
    alias="default",
    user='username',
    password='password',
    host='localhost',
    port='19530'
    )

    logging.warning("1.1")


    # def create_milvus_collection(collection_name, dim):
    #     logging.warning("1.2")
    #     if utility.has_collection(collection_name):
    #         utility.drop_collection(collection_name)
    #     logging.warning("1.3")
    #     fields = [
    #         FieldSchema(name='id', dtype=DataType.INT64, description='Ids', is_primary=True, auto_id=False),
    #         FieldSchema(name='text', dtype=DataType.VARCHAR, description='Page text', max_length=10000),
    #         FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Embedding vectors', dim=dim)
    #     ]
    #     logging.warning("1.4")
    #     schema = CollectionSchema(fields=fields, description="Spiritual search")
    #     collection = Collection(name=collection_name, schema=schema)

    #     index_params = {
    #         'metric_type': 'L2',
    #         'index_type': 'IVF_FLAT',
    #         'params': {"nlist": 2048}
    #     }

    #     collection.create_index(field_name="embedding", index_params=index_params)
    #     return collection


    # collectionName = "ruhnama"

    # collection = create_milvus_collection(collectionName, 1536)
    # print(collection.schema)



    # logging.warning("2")
    # for idx, line in enumerate(text):
    #     logging.warning("2.1")
    #     data = [[idx], [line], [embed(line)]]
    #     logging.warning("2.2")
    #     collection.insert(data)

    collection = Collection("ruhnama")

    collection.load()

    def search(text):
        search_params = {"metric_type": "L2"}
        results = collection.search(
            data=[embed(text)],
            anns_field="embedding",
            param=search_params,
            limit=5,
            output_fields=['text']
        )

        ret = []
        for hit in results[0]:
            row = []
            row.extend([hit.id, hit.score, hit.entity.get('text')])
            ret.append(row)
        return ret




    # search_terms = ["what is ruhnama"]
    # # for x in search_terms:
    # #     print("Search term: ", x)
    # #     for result in search(x):
    # #         print(result)


    limit = 3750

    logging.warning("2.3")
    def retrieve(query,contexts):
        prompt = ''
        logging.warning("2.4")
        prompt_start = ("Answer the question based on the context below. \n\n" + "Context:\n")
        prompt_end = (f"\n\nQuestion: {query}\nAnswer:")
        logging.warning("2.5")
        for i in range(0, len(contexts)):
            if len("\n\n---\n\n".join(contexts[:i])) >= limit:
                prompt = (prompt_start + "\n\n---\n\n".join(contexts[:i-1]) + prompt_end)
                break
            elif i == len(contexts)-1:
                prompt = (prompt_start + "\n\n---\n\n".join(contexts) + prompt_end)
        return prompt
    logging.warning("2.6")
    
    
    def performSearch(query):
        results = []
        logging.warning("2.7")
        for result in search(query):
            results.append(result[2])
        logging.warning("2.8")
        res = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = retrieve(query,results),
            temperature = 0,
            max_tokens = 400,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop = None
        )

        return {'res' : results, 'ans' : res["choices"][0]["text"]}

    # logging.warning("2.8")
    # print("----------------------------------------- Thinking... ------------------------------------------------------")
    # print(res["ans"])
    
    res = performSearch(question)
    answer = res["ans"]
    
    return answer

