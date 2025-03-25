# 🩺 MedQuery AI

## 🌟 Overview
MedQuery AI is an advanced AI-powered application that provides comprehensive medical insights through text queries and image analysis. Leveraging cutting-edge technologies like Retrieval-Augmented Generation (RAG), Google's Gemini AI, and Hugging Face embeddings, this tool offers intelligent medical information support.

## 🚀 Features
- **Text-Based Medical Queries**
  - Intelligent medical information retrieval
  - Web search integration for comprehensive insights
  - Contextual understanding of medical questions

- **Medical Image Analysis**
  - Advanced AI-powered medical image interpretation
  - Supports various medical image formats (PNG, JPG, JPEG)
  - Detailed symptom and condition detection

- **Multi-Modal Knowledge Base**
  - Utilizes Pinecone vector database
  - Combines structured medical knowledge with real-time web searches
  - Provides context-aware medical insights

## 🔄 Workflow
1. User submits a text query or medical image
2. Application processes input through RAG pipeline
3. AI retrieves and synthesizes relevant medical information
4. Results are presented with source references

## 🛠️ Installation

### Local Setup
1. Clone the repository
```bash
git clone https://github.com/RajIIITR/medical-knowledge-assistant.git
cd medical-knowledge-assistant
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Create a `.env` file in the project root
- Add necessary API keys for Google Generative AI and Pinecone

## 📌 Requirements
- Python 3.10
- Key dependencies:
  - sentence-transformers==2.2.2
  - langchain==0.3.1
  - pypdf==3.12.0 
  - python-dotenv==1.0.1
  - langchain-pinecone==0.2.3
  - langchain-community==0.3.1
  - langchain-experimental==0.0.1
  - langchain-google-genai==2.0.11
  - duckduckgo-search==7.5.3
  - torch==2.6.0 
  - torchaudio==2.6.0
  - torchvision==0.21.0

## ▶️ Usage
```bash
streamlit run app.py
```

### Text Query Mode
- Enter medical questions
- Receive AI-generated insights
- View supporting sources

### Image Analysis Mode
- Upload medical images
- Get AI-powered image interpretation
- Understand potential medical conditions

## 🌍 Deployment
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medqueryai.streamlit.app/)

**Live Demo:** https://medqueryai.streamlit.app/

### Deployment Options
- Streamlit Cloud
- AWS 
- Google Cloud Run

## ⚠️ Disclaimer
🚨 **Important Medical Notice:** 
This AI assistant provides informational support only. Always consult healthcare professionals for definitive medical advice, diagnosis, or treatment.

## 📄 Project Structure
```
GitInsight/
├── app.py                 # Main Streamlit application
├── src/
│   └── helper.py          # Helper functions for embeddings and repo processing
    └── prompt.py         
├── store_index.py         # Script to process and store code in Pinecone (First run this python file it stores data in chunks in vector database in our case PineCone.)
├── requirements.txt       # Dependencies
└── .env                   # Environment variables (not tracked)
```

---
⭐ **Star this repository** if you find it useful!
