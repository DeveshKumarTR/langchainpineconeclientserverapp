import pytest
from unittest.mock import patch, MagicMock
from client.client import LangChainPineconeClient
from client.utils.helpers import format_response, validate_file_type, get_user_input

class TestLangChainPineconeClient:
    """Test cases for the LangChain Pinecone client"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = LangChainPineconeClient("http://test-server:5000")
    
    @patch('requests.Session.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'healthy'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.health_check()
        assert result['status'] == 'healthy'
        mock_get.assert_called_once_with("http://test-server:5000/health")
    
    @patch('requests.Session.get')
    def test_health_check_failure(self, mock_get):
        """Test health check failure"""
        mock_get.side_effect = Exception("Connection failed")
        
        result = self.client.health_check()
        assert 'error' in result
        assert 'Health check failed' in result['error']
    
    @patch('os.path.exists')
    def test_upload_document_file_not_found(self, mock_exists):
        """Test upload with non-existent file"""
        mock_exists.return_value = False
        
        result = self.client.upload_document("/nonexistent/file.pdf")
        assert 'error' in result
        assert 'File not found' in result['error']
    
    @patch('os.path.exists')
    @patch('client.utils.helpers.validate_file_type')
    def test_upload_document_invalid_type(self, mock_validate, mock_exists):
        """Test upload with invalid file type"""
        mock_exists.return_value = True
        mock_validate.return_value = False
        
        result = self.client.upload_document("/path/to/file.xyz")
        assert 'error' in result
        assert 'File type not supported' in result['error']
    
    @patch('requests.Session.get')
    def test_list_documents(self, mock_get):
        """Test listing documents"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'documents': [{'doc_id': '123', 'filename': 'test.pdf'}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.list_documents()
        assert result['success'] is True
        assert len(result['documents']) == 1
    
    @patch('requests.Session.post')
    def test_search_documents(self, mock_post):
        """Test document search"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'query': 'test query',
            'results': [{'content': 'test content', 'similarity_score': 0.95}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.client.search_documents("test query", k=5)
        assert result['success'] is True
        assert result['query'] == 'test query'
        assert len(result['results']) == 1
    
    @patch('requests.Session.delete')
    def test_delete_document(self, mock_delete):
        """Test document deletion"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'success': True,
            'message': 'Document deleted successfully'
        }
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        result = self.client.delete_document("test-123")
        assert result['success'] is True
        assert 'deleted successfully' in result['message']

class TestHelpers:
    """Test cases for helper functions"""
    
    def test_validate_file_type_valid(self):
        """Test file type validation with valid types"""
        assert validate_file_type("document.pdf") is True
        assert validate_file_type("text.txt") is True
        assert validate_file_type("document.docx") is True
        assert validate_file_type("spreadsheet.xlsx") is True
    
    def test_validate_file_type_invalid(self):
        """Test file type validation with invalid types"""
        assert validate_file_type("image.jpg") is False
        assert validate_file_type("video.mp4") is False
        assert validate_file_type("archive.zip") is False
        assert validate_file_type("executable.exe") is False
    
    def test_format_response_error(self):
        """Test formatting error responses"""
        response = {"error": "Something went wrong"}
        result = format_response(response)
        assert "❌ Error:" in result
        assert "Something went wrong" in result
    
    def test_format_response_documents(self):
        """Test formatting document list responses"""
        response = {
            "success": True,
            "documents": [
                {
                    "doc_id": "123",
                    "filename": "test.pdf",
                    "chunk_count": 5,
                    "upload_time": "2024-01-01T00:00:00"
                }
            ]
        }
        result = format_response(response)
        assert "📁 Documents:" in result
        assert "test.pdf" in result
        assert "ID: 123" in result
    
    def test_format_response_search_results(self):
        """Test formatting search results"""
        response = {
            "success": True,
            "query": "test query",
            "results": [
                {
                    "content": "This is test content",
                    "similarity_score": 0.95,
                    "metadata": {"filename": "test.pdf"}
                }
            ]
        }
        result = format_response(response)
        assert "🔍 Search results" in result
        assert "test query" in result
        assert "Score: 0.950" in result
        assert "This is test content" in result
    
    def test_get_user_input_with_default(self):
        """Test get_user_input with default values"""
        # This would require mocking input(), which is complex
        # For now, just test the type conversion logic
        assert get_user_input("", int, 5) == 5
        assert get_user_input("", str, "default") == "default"
    
    def test_format_response_empty_documents(self):
        """Test formatting response with no documents"""
        response = {"success": True, "documents": []}
        result = format_response(response)
        assert "📁 No documents found" in result
