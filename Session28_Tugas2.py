import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import chromadb
from pinecone import Pinecone, ServerlessSpec

# =========================
# Load Environment Variables
# =========================
load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# =========================
# Load Dataset
# =========================
df = pd.read_csv("Data/data_mobil.csv")

# Combine text columns
df['text'] = (
    df['brand'].astype(str) + " " +
    df['model'].astype(str) + " " +
    df['specs'].astype(str) + " " +
    df['description'].astype(str)
)

# =========================
# TF-IDF Search
# =========================
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['text'])


def tfidf_search(query, top_k=5):
    q_vec = vectorizer.transform([query])
    sim = cosine_similarity(q_vec, tfidf_matrix).flatten()
    idx = sim.argsort()[-top_k:][::-1]

    return df.iloc[idx][['brand', 'model', 'price_idr', 'year']]


# =========================
# BM25 Search
# =========================
tokenized = [doc.split() for doc in df['text']]
bm25 = BM25Okapi(tokenized)


def bm25_search(query, top_k=5):
    scores = bm25.get_scores(query.split())
    idx = scores.argsort()[-top_k:][::-1]

    return df.iloc[idx][['brand', 'model', 'price_idr', 'year']]


# =========================
# Gemini Embedding
# =========================
def get_embedding(text):
        response = client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=text
        )
        return response.embeddings[0].values


# Generate embeddings if not exist
if 'embedding' not in df.columns:
    df['embedding'] = df['text'].apply(get_embedding)


# =========================
# ChromaDB Setup
# =========================
chroma_client = chromadb.Client()

collection_name = "mobil_gemini"

existing_collections = [col.name for col in chroma_client.list_collections()]

if collection_name in existing_collections:
    collection = chroma_client.get_collection(name=collection_name)
else:
    collection = chroma_client.create_collection(name=collection_name)

    for idx, row in df.iterrows():
        collection.add(
            ids=[str(idx)],
            embeddings=[list(row['embedding'])],
            metadatas=[{
                "brand": row['brand'],
                "model": row['model'],
                "price_idr": int(row['price_idr']),
                "year": int(row['year'])
            }],
            documents=[row['text']]
        )


# =========================
# Pinecone Setup
# =========================
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "mobil-gemini"
dimension = len(df['embedding'].iloc[0])

existing_indexes = [index.name for index in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)

# Upload data to Pinecone
batch_size = 8

for i in range(0, len(df), batch_size):
    end = min(i + batch_size, len(df))

    upsert_data = []

    for j in range(i, end):
        upsert_data.append(
            (
                str(j),
                list(df['embedding'].iloc[j]),
                {
                    "brand": str(df['brand'].iloc[j]),
                    "model": str(df['model'].iloc[j]),
                    "price_idr": int(df['price_idr'].iloc[j]),
                    "year": int(df['year'].iloc[j])
                }
            )
        )

    index.upsert(vectors=upsert_data)


# =========================
# Semantic Search Functions
# =========================
def semantic_search(query, top_k=5):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results['metadatas']



def pinecone_search(query, top_k=5):
    query_embedding = get_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results['matches']


# =========================
# Format Results
# =========================
def format_results(query, chroma_results, pinecone_results):
    def format_price(price):
        return f"Rp{price:,.0f}"

    output = []
    output.append(f"🔎 Query: {query}\n")

    # ChromaDB Results
    output.append("✅ ChromaDB Results")

    chroma_items = chroma_results[0] if chroma_results else []

    for item in chroma_items:
        output.append(
            f"- {item['brand']} {item['model']} | "
            f"{format_price(item['price_idr'])} | {item['year']}"
        )

    # Pinecone Results
    output.append("\n✅ Pinecone Results")

    for item in pinecone_results:
        meta = item['metadata']

        output.append(
            f"- {meta['brand']} {meta['model']} | "
            f"{format_price(meta['price_idr'])} | {meta['year']}"
        )

    return "\n".join(output)


# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="Car Search App", layout="wide")

st.title("🚗 Car Search App")
st.write("Keyword Search and Semantic Search using TF-IDF, BM25, ChromaDB, and Pinecone")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a search query.")

    else:
        st.subheader("TF-IDF Search Results")
        st.dataframe(tfidf_search(query))

        st.subheader("BM25 Search Results")
        st.dataframe(bm25_search(query))

        st.subheader("Semantic Search Results")

        chroma_results = semantic_search(query)
        pinecone_results = pinecone_search(query)

        # =========================
        # ChromaDB Table
        # =========================
        st.subheader("ChromaDB Search Results")

        chroma_items = chroma_results[0] if chroma_results else []

        chroma_df = pd.DataFrame(chroma_items)

        if not chroma_df.empty:
            st.dataframe(chroma_df)
        else:
            st.write("No ChromaDB results found.")


        # =========================
        # Pinecone Table
        # =========================
        st.subheader("Pinecone Search Results")

        pinecone_items = []

        for item in pinecone_results:
            meta = item["metadata"]

            pinecone_items.append({
                "brand": meta["brand"],
                "model": meta["model"],
                "price_idr": meta["price_idr"],
                "year": meta["year"],
                "score": item["score"]
            })

        pinecone_df = pd.DataFrame(pinecone_items)

        if not pinecone_df.empty:
            st.dataframe(pinecone_df)
        else:
            st.write("No Pinecone results found.")


