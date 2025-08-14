# Example Scripts and Usage

This directory contains example scripts showing how to use the LangChain Pinecone application.

## Server Examples

### Starting the Server in Production
```python
# production_server.py
from server.app import create_app
import os

if __name__ == "__main__":
    app = create_app('production')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Batch Document Processing
```python
# batch_upload.py
import os
import requests
from pathlib import Path

def batch_upload_directory(directory_path, server_url="http://127.0.0.1:5000"):
    """Upload all supported files in a directory"""
    directory = Path(directory_path)
    supported_extensions = {'.pdf', '.txt', '.docx', '.xlsx'}
    
    for file_path in directory.rglob('*'):
        if file_path.suffix.lower() in supported_extensions:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{server_url}/api/documents", files=files)
                if response.status_code == 201:
                    print(f"✅ Uploaded: {file_path.name}")
                else:
                    print(f"❌ Failed: {file_path.name} - {response.text}")

if __name__ == "__main__":
    batch_upload_directory("/path/to/documents")
```

## Client Examples

### Advanced Search with Filters
```python
# advanced_search.py
from client.client import LangChainPineconeClient

client = LangChainPineconeClient()

# Search with metadata filters
results = client.search_documents(
    query="artificial intelligence",
    k=10,
    filter_metadata={"filename": {"$regex": ".*research.*"}}
)

print(f"Found {len(results.get('results', []))} results")
for i, result in enumerate(results.get('results', []), 1):
    print(f"{i}. {result['metadata']['filename']}")
    print(f"   Score: {result['similarity_score']:.3f}")
    print(f"   Preview: {result['content'][:100]}...")
```

### Document Similarity Analysis
```python
# similarity_analysis.py
from client.client import LangChainPineconeClient

client = LangChainPineconeClient()

def analyze_document_similarity(doc_id):
    """Analyze similarity for a specific document"""
    similar_docs = client.find_similar_documents(doc_id, k=5)
    
    if 'error' in similar_docs:
        print(f"Error: {similar_docs['error']}")
        return
    
    print(f"Documents similar to {doc_id}:")
    for doc in similar_docs.get('similar_documents', []):
        print(f"- {doc['metadata']['filename']}")
        print(f"  Similarity: {doc['similarity_score']:.3f}")

# Usage
analyze_document_similarity("your-document-id-here")
```

### Automated Content Summarization
```python
# content_summarizer.py
from client.client import LangChainPineconeClient
import openai

client = LangChainPineconeClient()

def summarize_search_results(query, max_results=5):
    """Get search results and create a summary"""
    results = client.search_documents(query, k=max_results)
    
    if 'error' in results:
        return f"Error: {results['error']}"
    
    # Combine content from top results
    combined_content = ""
    for result in results.get('results', []):
        combined_content += result['content'] + "\n\n"
    
    # Create summary using OpenAI (requires openai library)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following content related to '{query}':\n\n{combined_content}",
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

# Usage
summary = summarize_search_results("machine learning algorithms")
print(summary)
```

## API Integration Examples

### JavaScript/Node.js Client
```javascript
// js_client.js
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class PineconeClient {
    constructor(baseUrl = 'http://127.0.0.1:5000') {
        this.baseUrl = baseUrl;
    }

    async uploadDocument(filePath) {
        const form = new FormData();
        form.append('file', fs.createReadStream(filePath));
        
        try {
            const response = await axios.post(
                `${this.baseUrl}/api/documents`,
                form,
                { headers: form.getHeaders() }
            );
            return response.data;
        } catch (error) {
            return { error: error.message };
        }
    }

    async searchDocuments(query, k = 5) {
        try {
            const response = await axios.post(`${this.baseUrl}/api/search`, {
                query,
                k
            });
            return response.data;
        } catch (error) {
            return { error: error.message };
        }
    }
}

// Usage
const client = new PineconeClient();
client.searchDocuments('artificial intelligence').then(results => {
    console.log(results);
});
```

### Python Async Client
```python
# async_client.py
import aiohttp
import asyncio
from typing import Dict, Any

class AsyncPineconeClient:
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')

    async def search_documents(self, session: aiohttp.ClientSession, query: str, k: int = 5) -> Dict[str, Any]:
        """Async document search"""
        async with session.post(
            f"{self.base_url}/api/search",
            json={"query": query, "k": k}
        ) as response:
            return await response.json()

    async def batch_search(self, queries: list) -> list:
        """Search multiple queries concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_documents(session, query) for query in queries]
            return await asyncio.gather(*tasks)

# Usage
async def main():
    client = AsyncPineconeClient()
    queries = ["machine learning", "data science", "artificial intelligence"]
    results = await client.batch_search(queries)
    
    for query, result in zip(queries, results):
        print(f"Query: {query}")
        print(f"Results: {len(result.get('results', []))}")

asyncio.run(main())
```

## Configuration Examples

### Custom Text Splitter
```python
# custom_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_custom_splitter():
    """Create a custom text splitter for specific document types"""
    return RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=["\n\n", "\n", ".", "!", "?", ";", " ", ""]
    )
```

### Environment-Specific Configurations
```python
# config_environments.py
import os

class DevelopmentConfig:
    DEBUG = True
    PINECONE_INDEX_NAME = "dev-langchain-docs"
    CHUNK_SIZE = 800  # Smaller chunks for testing

class ProductionConfig:
    DEBUG = False
    PINECONE_INDEX_NAME = "prod-langchain-docs"
    CHUNK_SIZE = 1200  # Larger chunks for production

class TestingConfig:
    TESTING = True
    PINECONE_INDEX_NAME = "test-langchain-docs"
    CHUNK_SIZE = 500  # Very small chunks for fast tests

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)
```
