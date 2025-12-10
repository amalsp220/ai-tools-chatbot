import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

# Configuration
CSV_PATH = "data/ai_tools.csv"
INDEX_DIR = "vectorstore"

def load_and_prepare_data():
    """
    Load the AIToolBuzz CSV and prepare documents for embedding.
    
    Returns:
        List of Document objects with metadata
    """
    print("Loading AI Tools dataset...")
    
    # Read the CSV file
    df = pd.read_csv(CSV_PATH)
    
    print(f"Loaded {len(df)} AI tools from dataset")
    
    # Drop rows with missing critical information
    df = df.dropna(subset=["Name"])
    
    # Fill NaN values with empty strings for other columns
    df = df.fillna("")
    
    print(f"Processing {len(df)} valid tools...")
    
    documents = []
    
    for idx, row in df.iterrows():
        # Create a comprehensive text representation of each tool
        text_content = f"""
Tool Name: {row.get('Name', '')}

Category: {row.get('Category', '')}

Primary Task: {row.get('Primary Task', '')}

Description: {row.get('Short Description', '')}

Keywords: {row.get('Keywords', '')}

Technologies: {row.get('technologies', '')}

Industry: {row.get('industry', '')}

Pricing: {row.get('Pricing', 'Not specified')}

Country: {row.get('Country', '')}

Year Founded: {row.get('Year Founded', '')}

Website: {row.get('Website', '')}
""".strip()
        
        # Create metadata dictionary
        metadata = {
            "name": str(row.get('Name', '')),
            "category": str(row.get('Category', '')),
            "primary_task": str(row.get('Primary Task', '')),
            "pricing": str(row.get('Pricing', 'Not specified')),
            "website": str(row.get('Website', '')),
            "country": str(row.get('Country', '')),
            "year_founded": str(row.get('Year Founded', '')),
            "technologies": str(row.get('technologies', '')),
        }
        
        # Create Document object
        doc = Document(
            page_content=text_content,
            metadata=metadata
        )
        documents.append(doc)
        
        # Progress indicator
        if (idx + 1) % 1000 == 0:
            print(f"Processed {idx + 1}/{len(df)} tools...")
    
    print(f"\nSuccessfully prepared {len(documents)} documents for embedding")
    return documents

def build_vectorstore(documents):
    """
    Build FAISS vectorstore from documents.
    
    Args:
        documents: List of Document objects
    """
    print("\nInitializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings()
    
    print("Building FAISS vectorstore (this may take a few minutes)...")
    print("Progress: Creating embeddings for all documents...")
    
    # Create vectorstore
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Save vectorstore locally
    print(f"\nSaving vectorstore to {INDEX_DIR}/...")
    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    
    print(f"✅ Vectorstore successfully saved to {INDEX_DIR}/")
    print(f"\n🎉 All done! You can now run the Streamlit app with: streamlit run app.py")

def main():
    """
    Main function to build the AI tools vectorstore.
    """
    print("✨ AIToolBuzz Vectorstore Builder ✨")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Check if CSV file exists
    if not os.path.exists(CSV_PATH):
        print(f"⚠️ Error: CSV file not found at {CSV_PATH}")
        print("\nPlease download the dataset from Kaggle:")
        print("  https://www.kaggle.com/datasets/devadigax/aitoolbuzz-com-16k-ai-tools-database/")
        print(f"\nAnd place it at: {CSV_PATH}")
        print("\nAlternatively, update the CSV_PATH variable in this script.")
        return
    
    try:
        # Load and prepare documents
        documents = load_and_prepare_data()
        
        # Build vectorstore
        build_vectorstore(documents)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("1. Your OpenAI API key is valid")
        print("2. The CSV file is in the correct format")
        print("3. You have sufficient disk space")
        import traceback
        print("\nFull error trace:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
