import pytest
import json
from unittest.mock import patch, MagicMock
from server.app import create_app

@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'PINECONE_API_KEY': 'test-key',
        'OPENAI_API_KEY': 'test-key',
        'PINECONE_INDEX_NAME': 'test-index'
    })
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'langchain-pinecone-server'

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Not found'

@patch('server.models.vector_store.VectorStoreManager')
def test_upload_document_no_file(mock_vector_store, client):
    """Test document upload with no file"""
    response = client.post('/api/documents')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'No file provided' in data['error']

@patch('server.models.vector_store.VectorStoreManager')
def test_upload_document_empty_filename(mock_vector_store, client):
    """Test document upload with empty filename"""
    data = {'file': (None, '')}
    response = client.post('/api/documents', data=data)
    assert response.status_code == 400
    
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert 'No file selected' in response_data['error']

@patch('server.models.vector_store.VectorStoreManager')
def test_list_documents(mock_vector_store, client):
    """Test listing documents"""
    # Mock the vector store manager
    mock_instance = MagicMock()
    mock_instance.list_documents.return_value = [
        {
            'doc_id': 'test-123',
            'filename': 'test.pdf',
            'upload_time': '2024-01-01T00:00:00',
            'chunk_count': 5
        }
    ]
    mock_vector_store.return_value = mock_instance
    
    response = client.get('/api/documents')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['documents']) == 1
    assert data['documents'][0]['doc_id'] == 'test-123'

@patch('server.models.vector_store.VectorStoreManager')
def test_search_documents_no_query(mock_vector_store, client):
    """Test search without query"""
    response = client.post('/api/search', json={})
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Query is required' in data['error']

@patch('server.models.vector_store.VectorStoreManager')
def test_search_documents_success(mock_vector_store, client):
    """Test successful document search"""
    # Mock the vector store manager
    mock_instance = MagicMock()
    mock_instance.similarity_search.return_value = [
        (MagicMock(page_content="Test content", metadata={"filename": "test.pdf"}), 0.95)
    ]
    mock_vector_store.return_value = mock_instance
    
    response = client.post('/api/search', json={'query': 'test query'})
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['query'] == 'test query'
    assert len(data['results']) == 1
    assert data['results'][0]['content'] == 'Test content'

@patch('server.models.vector_store.VectorStoreManager')
def test_delete_document(mock_vector_store, client):
    """Test document deletion"""
    # Mock the vector store manager
    mock_instance = MagicMock()
    mock_instance.delete_document.return_value = True
    mock_vector_store.return_value = mock_instance
    
    response = client.delete('/api/documents/test-123')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'deleted successfully' in data['message']

@patch('server.models.vector_store.VectorStoreManager')
def test_delete_document_not_found(mock_vector_store, client):
    """Test deleting non-existent document"""
    # Mock the vector store manager
    mock_instance = MagicMock()
    mock_instance.delete_document.return_value = False
    mock_vector_store.return_value = mock_instance
    
    response = client.delete('/api/documents/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Document not found' in data['error']

@patch('server.models.vector_store.VectorStoreManager')
def test_get_stats(mock_vector_store, client):
    """Test getting search statistics"""
    # Mock the vector store manager
    mock_instance = MagicMock()
    mock_instance.get_stats.return_value = {
        'total_vectors': 100,
        'dimension': 1536,
        'index_fullness': 0.05
    }
    mock_vector_store.return_value = mock_instance
    
    response = client.get('/api/search/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['stats']['total_vectors'] == 100
