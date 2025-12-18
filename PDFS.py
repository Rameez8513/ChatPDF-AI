import streamlit as st
# from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.memory.buffer import ConversationBufferMemory
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
import os
from htmlTemplates import css 
# load_dotenv()
OpenRoute_Api = st.secrets["OpenRoute_Api"]

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OpenRoute_Api,
        model="kwaipilot/kat-coder-pro:free", 
        temperature=0.7,
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        return True
    return False

def load_css():
    """Load CSS from external file"""
    try:
        with open("style.css", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback CSS if file not found
        return """
        <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
        }
        .main .block-container {
            padding-left: 340px !important;
        }
        </style>
        """

def main():
    # load_dotenv()
    st.set_page_config(
        page_title="PDF AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS from external file
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []
    if "last_question" not in st.session_state:
        st.session_state.last_question = ""
    
    # Sidebar with black gradient background
    with st.sidebar:
        # Header with logo and title
        st.markdown("""
            <div class="sidebar-header">
                <img src="https://img.icons8.com/fluency/96/pdf.png" alt="ChatPDF AI" class="sidebar-logo">
                <h1 class="sidebar-title">ChatPDF AI</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # File uploader
        st.subheader("📁 Upload Documents")
        pdf_docs = st.file_uploader(
            "Choose PDF files",
            accept_multiple_files=True,
            type=['pdf'],
            help="Select one or multiple PDF files"
        )
        
        if pdf_docs:
            st.info(f"📎 {len(pdf_docs)} file(s) selected")
        
        # Process button
        if st.button("⚡ Process Documents", use_container_width=True, type="primary"):
            if not pdf_docs:
                st.error("Please upload PDF files first!")
            else:
                with st.spinner(" Processing documents..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.session_state.processed_files = [pdf.name for pdf in pdf_docs]
                        st.success(" Processing complete!")
                        st.session_state.chat_history = None
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        # Processed files list
        if st.session_state.processed_files:
            st.markdown("---")
            st.markdown("### 📋 Processed Files")
            st.markdown('<div class="file-list">', unsafe_allow_html=True)
            for file in st.session_state.processed_files:
                st.markdown(f"""
                    <div class="file-item">
                        <span style="font-size: 18px;">📄</span>
                        <span>{file}</span>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Tips section
        st.markdown("""
            <div class="tips-container">
                <h3> How to Use</h3>
                <ul>
                    <li>Upload PDF documents</li>
                    <li>Click 'Process' to analyze</li>
                    <li>Ask questions about content</li>
                    <li>Get AI-powered answers</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Stats
        if st.session_state.processed_files:
            st.markdown("---")
            st.markdown("###  Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(st.session_state.processed_files)}</div>
                        <div class="metric-label">Files</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                chat_count = len(st.session_state.chat_history) if st.session_state.chat_history else 0
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{chat_count}</div>
                        <div class="metric-label">Messages</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = None
            st.session_state.last_question = ""
            st.rerun()
    
    # Main chat interface
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history is None or len(st.session_state.chat_history) == 0:
            # Welcome message
            st.markdown("""
                <div class="welcome-container">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0px; margin-bottom: 30px;">
                        <h1 class="welcome-title">ChatPDF AI</h1>
                    </div>
                    <p style="font-size: 18px; color: #6b7280; text-align: center; margin-bottom: 30px;">
                    Upload your PDF documents and have intelligent conversations with AI
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Messages container - SCROLLABLE AREA
            st.markdown('<div class="messages-scroll-wrapper">', unsafe_allow_html=True)
            st.markdown('<div class="messages-container">', unsafe_allow_html=True)
            # Display chat history
            for i, message in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    # AI message
                    st.markdown(f"""
                        <div class="message-wrapper ai-message">
                            <div class="message-content">
                                <div class="avatar">🤖</div>
                                <div class="message-bubble">
                                    {message.content}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                else:
                   # User message
                   st.markdown(f"""
                        <div class="message-wrapper user-message">
                            <div class="message-content">
                                <div class="message-bubble">
                                    {message.content}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)  # Close messages-container
            st.markdown('</div>', unsafe_allow_html=True)  # Close messages-scroll-wrapper
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
    
    # FIXED INPUT CONTAINER - WILL NOT MOVE WITH SCROLL
    st.markdown('<div class="fixed-input-wrapper">', unsafe_allow_html=True)
    
    # Use form for chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_question = st.text_input(
                "Message",
                placeholder="Ask a question about your PDFs...",
                label_visibility="collapsed",
                key="user_input"
            )
        
        with col2:
            submit_button = st.form_submit_button("➤", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close fixed-input-wrapper
    
    # Handle form submission
    if submit_button and user_question:
        if st.session_state.conversation is None:
            st.warning(" Please upload and process PDF documents first!")
        else:
            if user_question != st.session_state.get("last_question", ""):
                with st.spinner("ChatPDF AI beautifying Response.."):
                    if handle_userinput(user_question):
                        st.session_state.last_question = user_question
                        st.rerun()
            else:
                st.info("Question already processed.")

if __name__ == '__main__':
    main()