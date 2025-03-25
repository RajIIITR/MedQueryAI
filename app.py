import os
import io
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import base64

# Langchain imports
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Import helper functions
from src.helper import (
    download_hugging_face_embeddings, 
    preprocess_image, 
    perform_medical_web_search,
    format_web_sources,
    image_to_base64
)

# Load environment variables
load_dotenv()

# Configure Pinecone and create RAG pipeline
def initialize_rag_pipeline():
    try:
        # Download embeddings
        embeddings = download_hugging_face_embeddings()
        
        # Pinecone index details
        index_name = "medicalbot"
        
        # Initialize Pinecone Vector Store
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        
        # Configure retriever
        retriever = docsearch.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 3}
        )
        
        # Initialize Language Model
        llm = GoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.4
        )
        
        # Create a custom prompt template
        prompt_template = """Use the following pieces of context to answer the question. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}

        Helpful Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )
        
        # Create Retrieval QA Chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        return chain, llm
    
    except Exception as e:
        st.error(f"RAG Pipeline Initialization Error: {str(e)}")
        return None, None

# Text Query Page
def text_query_page(rag_chain):
    st.header("MedQuery AI")
    
    # Query input
    query = st.text_input("Enter your medical query:")
    
    if st.button("Get Medical Insights"):
        if not query:
            st.warning("Please enter a medical query")
            return
        
        with st.spinner("Analyzing your query..."):
            try:
                # Perform web search for additional context
                web_results = perform_medical_web_search(query)
                
                # Use RAG Chain for query
                if rag_chain:
                    # Combine query with additional context
                    full_query = f"{query}\n\nAdditional Context: {format_web_sources(web_results)}"
                    
                    # Get response
                    result = rag_chain({"query": full_query})
                    
                    # Display medical insights
                    st.markdown("### Medical Insights")
                    st.write(result['result'])
                    
                    # Display sources
                    with st.expander("Supporting Sources"):
                        # Show web search results
                        st.markdown("#### Web Sources")
                        for source in web_results:
                            st.markdown(f"- **{source['title']}**\n  {source['link']}")
                        
                        # Show source documents if available
                        st.markdown("#### Knowledge Base Sources")
                        if 'source_documents' in result:
                            for doc in result['source_documents']:
                                st.markdown(f"- {doc.page_content[:200]}...")
                
                else:
                    st.error("Could not initialize medical knowledge pipeline")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Image Analysis Page
def image_analysis_page(rag_chain, llm):
    st.header("Medical Image Analysis")
    
    # Image upload
    uploaded_image = st.file_uploader(
        "Upload a medical image", 
        type=['png', 'jpg', 'jpeg']
    )
    
    # Additional query about the image (optional)
    image_query = st.text_input(
        "Optional: Specific question about the image", 
        placeholder="What would you like to know about this medical image?"
    )
    
    if st.button("Analyze Image"):
        if uploaded_image is None:
            st.warning("Please upload a medical image")
            return
        
        with st.spinner("Analyzing image..."):
            try:
                # Open and preprocess image
                pil_image = Image.open(uploaded_image)
                processed_image = preprocess_image(pil_image)
                
                # Convert image to base64
                img_base64 = image_to_base64(processed_image)
                
                # Prepare image analysis prompt with strict medical relevance check
                image_analysis_prompt = f"""
                Imagine yourself as an experienced doctor or medical consultant. Provide a structured medical analysis of the patient's condition based on the image provided.
                
                ### Output Format:
                The analysis **must** be presented in a **clear and structured table format** with the following categories:

                | **Category**   | **Details** |
                |---------------|------------|
                | **Disease Name** | [Identify the possible disease based on the image] |
                | **Symptoms** | [List key symptoms observed] |
                | **Details** | [Provide a brief medical explanation] |
                | **Causes** | [List potential causes or risk factors] |
                | **Diagnosis** | [Suggest diagnostic methods] |
                | **Treatments** | [Mention standard treatments] |
                | **Medicine (Generic Name)** | [List medicine molecules or provide a prescription-style format] |
                | **Prevention** | [Give preventive measures] |

                ### Important Guidelines:
                - Ensure strict adherence to **table formatting**.
                - Use precise medical terminology.
                - Describe symptoms and findings objectively.
                - If uncertain, provide potential differentials rather than assuming a single diagnosis.

                At the end, mention: "**Consult an experienced doctor or medical consultant for further evaluation.**"

                **Image:** {img_base64}

                But if you don't know about the image or it seems irrelevant or doesn't matches medical relevance, please don't generate any analysis and respond as follows:
                "I don't know about this image" or "This image doesn't match medical relevance"
                """

                
                # Perform image analysis
                image_analysis = llm.invoke(image_analysis_prompt)
                
                # Display analysis results
                st.markdown("### Image Analysis")
                st.write(image_analysis)
                
                # Check if the image is actually medical
                if "Medical Relevance: Low" in image_analysis or "Not a Medical Image" in image_analysis:
                    st.warning("The uploaded image does not appear to be medically relevant.")
                    
                    # Optionally provide additional context about the image
                    st.info(f"Image Description: {image_analysis}")
                
            except Exception as e:
                st.error(f"Image analysis error: {e}")
                import traceback
                traceback.print_exc()

# Main Streamlit App
def main():
    # Page configuration
    st.set_page_config(
        page_title="MedQuery AI", 
        page_icon="🩺",
        layout="wide"
    )
    
    # Title
    st.title("🩺 MedQuery AI")
    
    # Initialize RAG Pipeline
    rag_chain, llm = initialize_rag_pipeline()
    
    # Page selection
    page = st.sidebar.radio(
        "Choose a Service", 
        ["Text Query", "Image Analysis"]
    )
    
    # Render appropriate page
    if page == "Text Query":
        text_query_page(rag_chain)
    else:
        image_analysis_page(rag_chain, llm)
    
    # Disclaimer
    st.sidebar.warning(
        "This AI provides informational support only. "
        "Always consult healthcare professionals for medical advice."
    )

# Run the Streamlit app
if __name__ == "__main__":
    main()