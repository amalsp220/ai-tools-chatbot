# 🤖 AI Tool Advisor

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Professional chatbot interface to explore and discover 16,000+ AI tools**

[Live Demo](#) • [Features](#features) • [Installation](#installation) • [Usage](#usage)

</div>

---

## 🎯 Overview

**AI Tool Advisor** is an intelligent chatbot that helps you discover and explore over 16,000 AI tools from the AIToolBuzz database. Built with modern RAG (Retrieval-Augmented Generation) architecture, it provides conversational AI assistance to find the perfect tools for your needs.

### ✨ Key Highlights

- 📚 **16,763 AI Tools**: Comprehensive database from AIToolBuzz.com
- 🤖 **Smart Recommendations**: GPT-3.5 powered conversational AI
- 🔍 **Vector Search**: Fast FAISS-based similarity search
- 🎨 **Beautiful UI**: Modern gradient design with Streamlit
- 💰 **Pricing Filters**: Find free, freemium, or paid tools
- 📊 **Source Tracking**: View data sources for transparency

## 🚀 Features

### Core Capabilities

- **Conversational Search**: Ask questions naturally and get AI-powered recommendations
- **Category Filtering**: Filter by pricing model (Free/Freemium/Paid)
- **Detailed Information**: Tool names, descriptions, pricing, use cases, and links
- **Chat History**: Maintains conversation context for follow-up questions
- **Suggested Prompts**: Quick-start queries for common use cases
- **Source Viewer**: Inspect the retrieved documents behind each answer

### Technical Features

- **RAG Architecture**: Combines vector search with GPT-3.5 for accurate answers
- **FAISS Vector Database**: Lightning-fast similarity search
- **OpenAI Embeddings**: High-quality text embeddings
- **LangChain Integration**: Robust conversation management
- **Streamlit Interface**: Responsive web-based UI

## 💻 Installation

### Prerequisites

- Python 3.10+
- OpenAI API Key
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/amalsp220/ai-tools-chatbot.git
cd ai-tools-chatbot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download Dataset

Download the AIToolBuzz dataset from Kaggle:

**Option A: Manual Download**
1. Visit [AIToolBuzz Dataset on Kaggle](https://www.kaggle.com/datasets/devadigax/aitoolbuzz-com-16k-ai-tools-database/)
2. Download the CSV file
3. Create `data/` folder and place the CSV as `data/ai_tools.csv`

**Option B: Using Kaggle API**
```bash
mkdir data
kaggle datasets download -d devadigax/aitoolbuzz-com-16k-ai-tools-database
unzip aitoolbuzz-com-16k-ai-tools-database.zip -d data/
mv data/*.csv data/ai_tools.csv
```

### Step 4: Set Up API Key

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

**Option B: .env File**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 5: Build Vector Index

```bash
python ingest.py
```

This will:
- Load the 16K+ AI tools dataset
- Generate embeddings using OpenAI
- Build and save the FAISS vectorstore (~5-10 minutes)

## 🎮 Usage

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Example Queries

Try these prompts:

- "Show me free AI image generators"
- "What are the best AI coding assistants for Python?"
- "Recommend AI tools for video editing and generation"
- "Find AI writing tools for content marketing"
- "Show me AI tools for data analysis"

### Using Filters

1. Open the sidebar
2. Select pricing models (Free/Freemium/Paid)
3. Ask your question
4. The AI will prioritize tools matching your filter

## 📚 Dataset

**Source**: [AIToolBuzz.com via Kaggle](https://www.kaggle.com/datasets/devadigax/aitoolbuzz-com-16k-ai-tools-database/)

**Statistics**:
- Total Tools: 16,763
- Collection Date: October 2025
- Update Frequency: Quarterly
- License: MIT / CC BY 4.0

**Columns**:
- Name, Category, Primary Task
- Short Description, Keywords
- Technologies, Industry
- Year Founded, Country
- Website, Pricing Model

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add `OPENAI_API_KEY` to app secrets
5. Deploy!

**Note**: Upload the pre-built `vectorstore/` folder to avoid rebuilding on every deployment.

### Other Platforms

- **Render**: Deploy as a web service
- **Railway**: One-click deployment
- **Heroku**: Use Procfile with `web: streamlit run app.py --server.port=$PORT`

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.29.0
- **LLM**: OpenAI GPT-3.5-turbo
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Framework**: LangChain 0.1.0
- **Language**: Python 3.10+

## 📁 Project Structure

```
ai-tools-chatbot/
├── app.py                 # Main Streamlit application
├── ingest.py              # Data ingestion & vectorstore builder
├── requirements.txt       # Python dependencies
├── data/
│   └── ai_tools.csv       # AIToolBuzz dataset (download separately)
├── vectorstore/           # FAISS index (generated by ingest.py)
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── README.md
└── LICENSE
```

## 💡 Tips & Best Practices

1. **Be Specific**: Instead of "AI tools", ask "AI tools for video editing"
2. **Use Filters**: Combine pricing filters with queries for better results
3. **Follow Up**: Ask clarifying questions to refine recommendations
4. **Explore Sources**: Click "View Sources" to see raw data
5. **Check Websites**: Verify pricing and features on official tool websites

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: [AIToolBuzz.com](https://aitoolbuzz.com/) for the comprehensive AI tools database
- **Kaggle**: [devadigax](https://www.kaggle.com/devadigax) for making the dataset available
- **Technologies**: Streamlit, LangChain, OpenAI, FAISS

## 💬 Support

For questions or issues:
- Open an [Issue](https://github.com/amalsp220/ai-tools-chatbot/issues)
- Contact: [Your Email/Contact]

---

<div align="center">

**Built with ❤️ by [Amal SP](https://github.com/amalsp220)**

⭐️ Star this repo if you find it helpful!

</div>
