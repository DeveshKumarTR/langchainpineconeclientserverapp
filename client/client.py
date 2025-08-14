import requests
import json
import os
from typing import List, Dict, Any, Optional
from client.utils.helpers import format_response, validate_file_type, get_user_input

class LangChainPineconeClient:
    """Client for interacting with the LangChain Pinecone server"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the server is running"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Health check failed: {str(e)}"}
    
    def upload_document(self, file_path: str) -> Dict[str, Any]:
        """Upload a document to the server"""
        try:
            if not os.path.exists(file_path):
                return {"error": "File not found"}
            
            if not validate_file_type(file_path):
                return {"error": "File type not supported"}
            
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = self.session.post(
                    f"{self.base_url}/api/documents",
                    files=files
                )
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            return {"error": f"Upload failed: {str(e)}"}
    
    def list_documents(self) -> Dict[str, Any]:
        """List all documents on the server"""
        try:
            response = self.session.get(f"{self.base_url}/api/documents")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to list documents: {str(e)}"}
    
    def search_documents(
        self, 
        query: str, 
        k: int = 5, 
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search documents using similarity search"""
        try:
            data = {
                "query": query,
                "k": k
            }
            if filter_metadata:
                data["filter"] = filter_metadata
            
            response = self.session.post(
                f"{self.base_url}/api/search",
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"error": f"Search failed: {str(e)}"}
    
    def find_similar_documents(self, doc_id: str, k: int = 5) -> Dict[str, Any]:
        """Find documents similar to a given document"""
        try:
            data = {
                "doc_id": doc_id,
                "k": k
            }
            
            response = self.session.post(
                f"{self.base_url}/api/search/similar",
                json=data
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            return {"error": f"Similar search failed: {str(e)}"}
    
    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document from the server"""
        try:
            response = self.session.delete(f"{self.base_url}/api/documents/{doc_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Delete failed: {str(e)}"}
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        try:
            response = self.session.get(f"{self.base_url}/api/search/stats")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to get stats: {str(e)}"}

def interactive_mode():
    """Run the client in interactive mode"""
    client = LangChainPineconeClient()
    
    print("=== LangChain Pinecone Client ===")
    print("Checking server connection...")
    
    health = client.health_check()
    if "error" in health:
        print(f"❌ Server connection failed: {health['error']}")
        return
    
    print("✅ Server is running!")
    print("\nAvailable commands:")
    print("1. upload - Upload a document")
    print("2. list - List all documents")
    print("3. search - Search documents")
    print("4. similar - Find similar documents")
    print("5. delete - Delete a document")
    print("6. stats - Show statistics")
    print("7. quit - Exit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit" or command == "q":
                print("Goodbye!")
                break
            
            elif command == "upload" or command == "1":
                file_path = input("Enter file path: ").strip()
                result = client.upload_document(file_path)
                print(format_response(result))
            
            elif command == "list" or command == "2":
                result = client.list_documents()
                print(format_response(result))
            
            elif command == "search" or command == "3":
                query = input("Enter search query: ").strip()
                k = get_user_input("Number of results (default 5): ", int, 5)
                result = client.search_documents(query, k)
                print(format_response(result))
            
            elif command == "similar" or command == "4":
                doc_id = input("Enter document ID: ").strip()
                k = get_user_input("Number of results (default 5): ", int, 5)
                result = client.find_similar_documents(doc_id, k)
                print(format_response(result))
            
            elif command == "delete" or command == "5":
                doc_id = input("Enter document ID to delete: ").strip()
                confirm = input(f"Are you sure you want to delete {doc_id}? (y/N): ").strip().lower()
                if confirm == 'y' or confirm == 'yes':
                    result = client.delete_document(doc_id)
                    print(format_response(result))
                else:
                    print("Delete cancelled.")
            
            elif command == "stats" or command == "6":
                result = client.get_search_stats()
                print(format_response(result))
            
            else:
                print("Unknown command. Type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    interactive_mode()
