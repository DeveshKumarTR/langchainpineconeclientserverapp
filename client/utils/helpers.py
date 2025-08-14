import json
import os
from typing import Any, Dict, Type, Optional

def format_response(response: Dict[str, Any]) -> str:
    """Format API response for display"""
    if "error" in response:
        return f"❌ Error: {response['error']}"
    
    if "success" in response and response["success"]:
        if "documents" in response:
            # List documents response
            documents = response["documents"]
            if not documents:
                return "📁 No documents found"
            
            result = "📁 Documents:\n"
            for doc in documents:
                result += f"  • {doc.get('filename', 'Unknown')} (ID: {doc.get('doc_id', 'N/A')})\n"
                result += f"    Chunks: {doc.get('chunk_count', 0)}, "
                result += f"Uploaded: {doc.get('upload_time', 'Unknown')}\n"
            return result
        
        elif "results" in response:
            # Search results response
            results = response["results"]
            if not results:
                return f"🔍 No results found for query: '{response.get('query', '')}'"
            
            result = f"🔍 Search results for '{response.get('query', '')}':\n"
            for i, res in enumerate(results, 1):
                result += f"\n{i}. Score: {res.get('similarity_score', 0):.3f}\n"
                result += f"   Content: {res.get('content', '')[:200]}...\n"
                metadata = res.get('metadata', {})
                if metadata:
                    result += f"   File: {metadata.get('filename', 'Unknown')}\n"
            return result
        
        elif "similar_documents" in response:
            # Similar documents response
            docs = response["similar_documents"]
            if not docs:
                return f"🔍 No similar documents found for ID: {response.get('reference_doc_id', '')}"
            
            result = f"🔍 Similar to document {response.get('reference_doc_id', '')}:\n"
            for i, doc in enumerate(docs, 1):
                result += f"\n{i}. Score: {doc.get('similarity_score', 0):.3f}\n"
                result += f"   Content: {doc.get('content', '')[:200]}...\n"
                metadata = doc.get('metadata', {})
                if metadata:
                    result += f"   File: {metadata.get('filename', 'Unknown')}\n"
            return result
        
        elif "stats" in response:
            # Statistics response
            stats = response["stats"]
            result = "📊 Vector Store Statistics:\n"
            result += f"  • Total vectors: {stats.get('total_vectors', 0)}\n"
            result += f"  • Dimension: {stats.get('dimension', 0)}\n"
            result += f"  • Index fullness: {stats.get('index_fullness', 0):.2%}\n"
            return result
        
        elif "doc_id" in response:
            # Upload response
            return (f"✅ Document uploaded successfully!\n"
                   f"  • File: {response.get('filename', 'Unknown')}\n"
                   f"  • Document ID: {response.get('doc_id', 'N/A')}\n"
                   f"  • Chunks created: {response.get('chunks_created', 0)}")
        
        elif "message" in response:
            # Generic success message
            return f"✅ {response['message']}"
    
    # Fallback: pretty print the entire response
    return json.dumps(response, indent=2)

def validate_file_type(file_path: str) -> bool:
    """Validate if file type is supported"""
    allowed_extensions = {'.pdf', '.txt', '.docx', '.xlsx'}
    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in allowed_extensions

def get_user_input(prompt: str, input_type: Type = str, default: Any = None) -> Any:
    """Get user input with type conversion and default value"""
    try:
        user_input = input(prompt).strip()
        
        if not user_input and default is not None:
            return default
        
        if input_type == int:
            return int(user_input)
        elif input_type == float:
            return float(user_input)
        elif input_type == bool:
            return user_input.lower() in ('true', '1', 'yes', 'y')
        else:
            return user_input
    
    except (ValueError, TypeError):
        if default is not None:
            print(f"Invalid input, using default: {default}")
            return default
        raise

def print_banner():
    """Print application banner"""
    banner = """
    ╭─────────────────────────────────────────╮
    │     LangChain Pinecone Vector Store     │
    │              Client Application         │
    ╰─────────────────────────────────────────╯
    """
    print(banner)

def print_help():
    """Print help information"""
    help_text = """
Available Commands:
  upload    - Upload and process a document
  list      - List all processed documents  
  search    - Search documents using semantic search
  similar   - Find documents similar to a given document
  delete    - Delete a document and all its chunks
  stats     - Show vector store statistics
  help      - Show this help message
  quit      - Exit the application

File Types Supported:
  • PDF (.pdf)
  • Text files (.txt)
  • Word documents (.docx)
  • Excel files (.xlsx)

Examples:
  upload /path/to/document.pdf
  search "artificial intelligence"
  similar abc123-def456-ghi789
    """
    print(help_text)
