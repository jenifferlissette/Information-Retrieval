

import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pandas as pd

# Inicializar el tokenizador y el modelo BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained('bert-base-uncased')

def generate_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='tf', padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()  # Use [CLS] token representation

def generate_bert_embeddings_parallel(texts, batch_size=100):
    with Pool(processes=cpu_count()) as pool:
        embeddings = []
        for i in tqdm(range(0, len(texts), batch_size), desc="Generando embeddings"):
            batch = texts[i:i+batch_size]
            batch_embeddings = pool.map(generate_bert_embedding, batch)
            embeddings.extend(batch_embeddings)
    return np.array(embeddings).squeeze()

if __name__ == '__main__':

    wine_df = pd.read_csv(r"C:\Users\VELA\Desktop\Recuperacion\Information-Retrieval\data\winemag-data_first150k.csv")
    print(wine_df.head())
    corpus = wine_df['description']
    
    bert_embeddings = generate_bert_embeddings_parallel(corpus)
    print("BERT Embeddings:", bert_embeddings)
    print("BERT Shape:", bert_embeddings.shape)