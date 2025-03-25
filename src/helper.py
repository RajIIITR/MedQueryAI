import os
from typing import List, Dict
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from duckduckgo_search import DDGS
import requests
from io import BytesIO
from PIL import Image
import base64

def load_pdf_file(data):
    """Load PDF files from a directory"""
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def text_split(extracted_data):
    """Split documents into text chunks"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def download_hugging_face_embeddings():
    """Download HuggingFace embeddings"""
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

def perform_medical_web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform web search using DuckDuckGo with medical domain focus
    """
    medical_domains = [
        'mayoclinic.org', 
        'healthline.com', 
        'webmd.com', 
        'medlineplus.gov', 
        'nih.gov', 
        'who.int', 
        'cdc.gov', 
        'nhs.uk',
        'wikipedia.org' 
    ]
    
    results = []
    with DDGS(timeout=20) as ddgs:
        search_query = f"site:({' OR '.join(medical_domains)}) {query}"
        for result in ddgs.text(search_query, max_results=max_results):
            try:
                results.append({
                    'title': result.get('title', 'Untitled Medical Source'),
                    'link': result.get('href', ''),
                    'snippet': result.get('body', 'No excerpt available')
                })
            except Exception as e:
                print(f"Search result processing error: {e}")
        
    return results

def download_image(image_url: str) -> Image.Image:
    """Download image from URL"""
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def preprocess_image(image: Image.Image, max_size: tuple = (224, 224)) -> Image.Image:
    """Preprocess image for model input"""
    if image is None:
        return None
    
    # Resize image maintaining aspect ratio
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    return image

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 encoded string"""
    if image is None:
        return None
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def format_web_sources(web_results: List[Dict[str, str]]) -> str:
    """
    Format web search results into a readable string for context
    """
    if not web_results:
        return "No external sources found."
    
    formatted_sources = "Supporting Medical Sources:\n"
    for i, source in enumerate(web_results, 1):
        formatted_sources += f"{i}. {source['title']}\n"
        formatted_sources += f"   Link: {source['link']}\n"
        formatted_sources += f"   Excerpt: {source['snippet'][:200]}...\n\n"
    
    return formatted_sources
