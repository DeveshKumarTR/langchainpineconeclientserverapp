# Installation and Setup Guide

## Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **Pinecone Account** - Sign up at [pinecone.io](https://www.pinecone.io/)
3. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)

## Quick Start

### 1. Environment Setup

```bash
# Clone or navigate to the project directory
cd pinecone

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your API keys:
# PINECONE_API_KEY=your_pinecone_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
# PINECONE_INDEX_NAME=langchain-documents
```

### 3. Initialize Pinecone Index

```bash
# Initialize the vector database
python -m flask --app server.app init-db
```

### 4. Start the Server

```bash
# Run the Flask server
python server/app.py
```

The server will start on `http://127.0.0.1:5000`

### 5. Use the Client

```bash
# In a new terminal, run the client
python client/client.py
```

## API Usage Examples

### Upload a Document
```bash
curl -X POST -F "file=@document.pdf" http://127.0.0.1:5000/api/documents
```

### Search Documents
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "k": 5}' \
  http://127.0.0.1:5000/api/search
```

### List Documents
```bash
curl http://127.0.0.1:5000/api/documents
```

## Client Application Features

The interactive client provides:
- Document upload and processing
- Semantic search across documents  
- Similar document discovery
- Document management (list, delete)
- Vector store statistics

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Errors**: Check your `.env` file configuration
3. **Pinecone Index Errors**: Initialize the index using the Flask CLI command
4. **File Upload Errors**: Check file type and size limits

### Supported File Types
- PDF (.pdf)
- Text files (.txt)  
- Word documents (.docx)
- Excel files (.xlsx)

### Configuration Options

Edit `.env` file to customize:
- `CHUNK_SIZE` - Text chunk size for processing (default: 1000)
- `CHUNK_OVERLAP` - Overlap between chunks (default: 200)  
- `MAX_FILE_SIZE` - Maximum upload size in bytes (default: 16MB)
- `FLASK_PORT` - Server port (default: 5000)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

### Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `PINECONE_API_KEY` | Yes | Pinecone API key | None |
| `OPENAI_API_KEY` | Yes | OpenAI API key | None |
| `PINECONE_INDEX_NAME` | No | Pinecone index name | langchain-documents |
| `PINECONE_ENVIRONMENT` | No | Pinecone environment | us-west1-gcp-free |
| `FLASK_PORT` | No | Server port | 5000 |
| `FLASK_HOST` | No | Server host | 127.0.0.1 |
| `CHUNK_SIZE` | No | Text chunk size | 1000 |
| `CHUNK_OVERLAP` | No | Chunk overlap | 200 |
