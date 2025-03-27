# 🩺 MedQuery AI: Advanced Medical Knowledge Assistant

## 🌟 Project Overview

MedQuery AI is a sophisticated medical assistant leveraging Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware medical insights through text queries and image analysis.

## 🚀 Workflow Overview

### 1️⃣ Initializing the RAG Pipeline

#### Environment and Setup
- **Environment Variables**: Loaded using `dotenv`
- **Embeddings**: `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`)
- **Vector Store**: Pinecone with `medicalbot` index
- **Language Model**: Google Gemini 2.0 Flash
- **Retrieval**: Similarity search with `k=3` most relevant documents

### 2️⃣ Text Query Processing

1. **User Query Input**
   - Medical-related questions accepted
   - DuckDuckGo web search on trusted medical sites
   - Contextual information from Mayo Clinic, WebMD, NIH, WHO

2. **Answer Generation**
   - RAG model processes enhanced query
   - Gemini AI generates evidence-based response
   - Output includes medical insights and source references

### 3️⃣ Medical Image Analysis

1. **Image Upload**
   - Supports PNG, JPG, JPEG
   - Preprocessing: 224x224 pixel resize, RGB conversion

2. **AI-Powered Analysis**
   - Structured medical analysis template:
     * Disease Name
     * Symptoms
     * Details
     * Causes
     * Diagnosis
     * Treatments
     * Generic Medicines
     * Prevention

## 🛠️ Core Functionalities

### Text Processing
- `load_pdf_file()`: Medical PDF document retrieval
- `text_split()`: Text chunk processing
- `download_hugging_face_embeddings()`: Semantic search embeddings

### Web Search
- `perform_medical_web_search()`: DuckDuckGo medical information retrieval
- `format_web_sources()`: Search result formatting

### Image Processing
- `download_image()`: Image URL handling
- `preprocess_image()`: Image preparation for analysis
- `image_to_base64()`: LLM image input conversion

## 📌 Prompts and Response Strategy

### Medical Assistant Prompt
- Structured, evidence-based responses
- Comprehensive medical information coverage
- Disclaimer: Always consult a healthcare professional

### Image Analysis Prompt
- Strict medical image analysis
- Refusal of irrelevant image processing

## 🌍 User Interface

**Streamlit-Powered UI**
- Sidebar Navigation
  * Text Query Mode
  * Image Analysis Mode
- Dynamic Result Presentation

## 🆕 Version Enhancements

- ✅ DuckDuckGo Search Integration
- ✅ Medical Image Analysis
- ✅ Structured AI Responses
- ✅ Intuitive Streamlit Interface

## ⚠️ Critical Disclaimer

🚨 **MedQuery AI provides informational support only. It is NOT a substitute for professional medical advice. Always consult a qualified healthcare expert.** 🚨