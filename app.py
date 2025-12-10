import os
import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Page configuration
st.set_page_config(
    page_title="AI Tool Advisor - Chat with 16K+ AI Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, professional look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 3em;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .tool-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_vectorstore():
    """Load the FAISS vectorstore with AI tools data"""
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            "vectorstore", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    except Exception as e:
        st.error(f"Error loading vectorstore: {str(e)}")
        st.info("Please make sure you've run ingest.py first to build the index.")
        return None

@st.cache_resource
def get_conversation_chain(_vectorstore):
    """Create the conversational chain"""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Custom prompt template
    template = """
You are an expert AI tools advisor with deep knowledge of 16,000+ AI tools.
Use the following context to answer questions about AI tools.

Context: {context}

Chat History: {chat_history}

Question: {question}

Instructions:
1. Recommend 3-7 relevant AI tools based on the user's needs
2. For each tool, provide:
   - Name
   - Brief description (1-2 sentences)
   - Primary use case
   - Pricing model (Free/Freemium/Paid)
   - Key features or technologies
3. Be conversational and helpful
4. If unsure, admit it and suggest alternatives
5. Format your response in a clear, readable way

Answer:"""
    
    retriever = _vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False
    )
    
    return chain

def main():
    # Header
    st.markdown("<h1>🤖 AI Tool Advisor</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: white; font-size: 1.2em;'>"
        "Chat with 16,000+ AI tools from AIToolBuzz database"
        "</p>", 
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.title("🔧 Settings")
        
        st.markdown("### 📊 Dataset Info")
        st.info("""
        **16,763 AI Tools**
        
        Source: AIToolBuzz.com via Kaggle
        
        Categories: Communication, Content Creation, Development, Marketing, and more.
        """)
        
        st.markdown("### 🎯 Quick Filters")
        pricing_filter = st.multiselect(
            "Pricing Model",
            ["Free", "Freemium", "Paid", "Contact for Pricing"],
            default=[]
        )
        
        st.markdown("### 💡 Suggested Prompts")
        if st.button("🎨 Free AI image generators"):
            st.session_state.suggested_prompt = "Show me free AI image generators"
        if st.button("💻 AI coding assistants"):
            st.session_state.suggested_prompt = "What are the best AI coding assistants?"
        if st.button("📝 AI writing tools"):
            st.session_state.suggested_prompt = "Recommend AI writing and content creation tools"
        if st.button("🎥 Video generation tools"):
            st.session_state.suggested_prompt = "AI tools for video generation and editing"
        
        st.markdown("---")
        st.markdown("""
        ### 🚀 About
        Built with:
        - Streamlit
        - LangChain
        - OpenAI GPT-3.5
        - FAISS Vector DB
        
        [GitHub Repository](https://github.com/amalsp220/ai-tools-chatbot)
        """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation" not in st.session_state:
        with st.spinner("Loading AI Tools database..."):
            vectorstore = load_vectorstore()
            if vectorstore:
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.session_state.vectorstore_loaded = True
            else:
                st.session_state.vectorstore_loaded = False
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggested prompts
    if "suggested_prompt" in st.session_state:
        user_input = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
    else:
        user_input = st.chat_input("Ask me about AI tools... (e.g., 'Best free AI tools for startups')")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        if st.session_state.get("vectorstore_loaded", False):
            with st.chat_message("assistant"):
                with st.spinner("Searching through 16K+ AI tools..."):
                    try:
                        # Add pricing filter to query if selected
                        query = user_input
                        if pricing_filter:
                            query += f" Only show tools with pricing: {', '.join(pricing_filter)}."
                        
                        response = st.session_state.conversation({"question": query})
                        answer = response["answer"]
                        
                        st.markdown(answer)
                        
                        # Show source documents in expander
                        if "source_documents" in response:
                            with st.expander("📚 View Sources"):
                                for i, doc in enumerate(response["source_documents"][:5]):
                                    st.markdown(f"**Source {i+1}:**")
                                    st.text(doc.page_content[:300] + "...")
                                    st.markdown("---")
                        
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            st.error("Vectorstore not loaded. Please check the setup.")

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY") and not st.secrets.get("OPENAI_API_KEY"):
        st.error("""
        ⚠️ OpenAI API key not found!
        
        Please set your API key:
        - Locally: Set OPENAI_API_KEY environment variable
        - Streamlit Cloud: Add OPENAI_API_KEY to your app secrets
        """)
        st.stop()
    
    main()
