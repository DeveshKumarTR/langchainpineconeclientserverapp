# LangChain Pinecone Vector Database Application

A Flask-based client-server application using LangChain and Pinecone vector database for document embedding, storage, and semantic retrieval.

## ✨ Features

- **Document Processing**: Upload and process documents (PDF, TXT, DOCX, XLSX) using LangChain
- **Vector Storage**: Store document embeddings in Pinecone vector database
- **Semantic Search**: Search documents using vector similarity
- **REST API**: Flask-based API for client-server communication
- **Interactive Client**: Python client for easy interaction with the server
- **Batch Operations**: Support for bulk document processing
- **Similarity Analysis**: Find documents similar to a given document

## 🏗️ Project Structure

```
├── server/
│   ├── app.py              # Flask server application
│   ├── config.py           # Configuration settings
│   ├── models/
│   │   └── vector_store.py # Pinecone vector store implementation
│   └── routes/
│       ├── __init__.py
│       ├── documents.py    # Document upload/processing endpoints
│       └── search.py       # Search endpoints
├── client/
│   ├── client.py           # Client application
│   └── utils/
│       └── helpers.py      # Client utility functions
├── config/
│   └── settings.py         # Global configuration
├── tests/
│   ├── test_server.py      # Server tests
│   └── test_client.py      # Client tests
├── examples/
│   └── README.md           # Usage examples and scripts
├── requirements.txt        # Project dependencies
├── .env.example           # Environment variables template
├── INSTALL.md             # Detailed setup instructions
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed on your system
- Pinecone API key ([Get one here](https://www.pinecone.io/))
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Setup Environment
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
# Edit .env with your API keys
```

### 2. Initialize Vector Database
```bash
# Initialize Pinecone index
python -m flask --app server.app init-db
```

### 3. Start the Server
```bash
python server/app.py
```

### 4. Use the Client
```bash
# In a new terminal
python client/client.py
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/documents` | Upload and process documents |
| `GET` | `/api/documents` | List processed documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |
| `POST` | `/api/search` | Search documents by query |
| `POST` | `/api/search/similar` | Find similar documents |
| `GET` | `/api/search/stats` | Get vector store statistics |

## 🔧 Configuration

Key environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PINECONE_API_KEY` | ✅ | - | Your Pinecone API key |
| `OPENAI_API_KEY` | ✅ | - | Your OpenAI API key |
| `PINECONE_INDEX_NAME` | ❌ | `langchain-documents` | Pinecone index name |
| `CHUNK_SIZE` | ❌ | `1000` | Text chunk size for processing |
| `CHUNK_OVERLAP` | ❌ | `200` | Overlap between text chunks |
| `FLASK_PORT` | ❌ | `5000` | Server port |

## 📖 Usage Examples

### Upload a Document
```python
from client.client import LangChainPineconeClient

client = LangChainPineconeClient()
result = client.upload_document("path/to/document.pdf")
print(result)
```

### Search Documents
```python
results = client.search_documents("machine learning", k=5)
for result in results['results']:
    print(f"Score: {result['similarity_score']:.3f}")
    print(f"Content: {result['content'][:100]}...")
```

### API Usage with cURL
```bash
# Upload document
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/documents

# Search documents
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence", "k": 5}' \
  http://127.0.0.1:5000/api/search
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=server --cov=client
```

## 📁 Supported File Types

- **PDF** (.pdf) - Portable Document Format
- **Text** (.txt) - Plain text files
- **Word** (.docx) - Microsoft Word documents
- **Excel** (.xlsx) - Microsoft Excel spreadsheets

## 🛠️ Development

### Code Formatting
```bash
black .
flake8 .
```

### Adding New Features
1. Add endpoints in `server/routes/`
2. Update the vector store model in `server/models/vector_store.py`
3. Add client methods in `client/client.py`
4. Write tests in `tests/`

## 📚 Documentation

- **[Installation Guide](INSTALL.md)** - Detailed setup instructions
- **[Examples](examples/README.md)** - Usage examples and scripts
- **[API Documentation](#-api-endpoints)** - REST API reference

## 🔍 Troubleshooting

### Common Issues

**Python not found**: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)

**API key errors**: Check your `.env` file configuration

**Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Pinecone connection issues**: Verify your API key and index name

See [INSTALL.md](INSTALL.md) for detailed troubleshooting guide.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Built with**: Flask, LangChain, Pinecone, OpenAI
