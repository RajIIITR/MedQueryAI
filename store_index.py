from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone  # Updated import
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

'''
Load dataset n its chunk which we could then pass our chunks to embedding model which gives vector 
representation of each chunk we will store it in vector database in our case it is PineCone.
Our goal is to use pinecone or any other vector database so that on the basis of semantic search
It will return the relevant data to the user or we can say similar data on the basis of similarity score.
'''

extracted_data = load_pdf_file(data='Data/')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

# Initialize Pinecone with the new SDK approach
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalbot"

'''
The role of below code is that it automatically create pinecone index in our Pinecone website where is stores
embedding of our chunks
'''

# Create index with the updated API
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec={
            "serverless": {
                "cloud": "aws",
                "region": "us-east-1"
            }
        }
    )

# Embed each chunk and upsert the embeddings into your Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)