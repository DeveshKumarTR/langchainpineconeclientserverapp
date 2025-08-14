import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from flask import current_app
import logging
from typing import List, Dict, Any, Tuple, Optional
from langchain_core.documents import Document

class VectorStoreManager:
    """Manages Pinecone vector store operations for LangChain"""
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.pc = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Pinecone and embeddings"""
        try:
            # Initialize Pinecone
            self.pc = pinecone.Pinecone(
                api_key=current_app.config['PINECONE_API_KEY']
            )
            
            # Initialize OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=current_app.config['OPENAI_API_KEY']
            )
            
            # Get or create index
            index_name = current_app.config['PINECONE_INDEX_NAME']
            
            if index_name in [index.name for index in self.pc.list_indexes()]:
                index = self.pc.Index(index_name)
                self.vector_store = Pinecone(index, self.embeddings.embed_query, "text")
            else:
                logging.warning(f"Index {index_name} not found. Call init_index() to create it.")
            
        except Exception as e:
            logging.error(f"Failed to initialize vector store: {str(e)}")
            raise
    
    def init_index(self, dimension: int = 1536):
        """Initialize Pinecone index"""
        try:
            index_name = current_app.config['PINECONE_INDEX_NAME']
            
            # Check if index already exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if index_name not in existing_indexes:
                # Create new index
                self.pc.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric='cosine'
                )
                logging.info(f"Created Pinecone index: {index_name}")
            
            # Initialize vector store
            index = self.pc.Index(index_name)
            self.vector_store = Pinecone(index, self.embeddings.embed_query, "text")
            
        except Exception as e:
            logging.error(f"Failed to initialize index: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            # Add documents and return IDs
            ids = self.vector_store.add_documents(documents)
            logging.info(f"Added {len(documents)} documents to vector store")
            return ids
            
        except Exception as e:
            logging.error(f"Failed to add documents: {str(e)}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5, 
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
            
            return results
            
        except Exception as e:
            logging.error(f"Failed to perform similarity search: {str(e)}")
            raise
    
    def find_similar_documents(
        self, 
        doc_id: str, 
        k: int = 5
    ) -> List[Tuple[Document, float]]:
        """Find documents similar to a given document"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            # First, find the document by ID
            filter_dict = {"doc_id": doc_id}
            reference_docs = self.vector_store.similarity_search(
                query="",  # Empty query since we're filtering by ID
                k=1,
                filter=filter_dict
            )
            
            if not reference_docs:
                raise ValueError(f"Document with ID {doc_id} not found")
            
            # Use the content of the reference document to find similar ones
            reference_content = reference_docs[0].page_content
            
            # Search for similar documents, excluding the reference document itself
            results = self.similarity_search(
                query=reference_content,
                k=k + 1,  # Get one extra to exclude the reference
                filter={"doc_id": {"$ne": doc_id}}  # Exclude the reference document
            )
            
            return results[:k]  # Return only k results
            
        except Exception as e:
            logging.error(f"Failed to find similar documents: {str(e)}")
            raise
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete all chunks of a document"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            # Get the index directly for deletion operations
            index = self.pc.Index(current_app.config['PINECONE_INDEX_NAME'])
            
            # Query for all vectors with the specified doc_id
            query_result = index.query(
                filter={"doc_id": doc_id},
                top_k=10000,  # Get all matching vectors
                include_metadata=True
            )
            
            if not query_result.matches:
                return False
            
            # Extract IDs to delete
            ids_to_delete = [match.id for match in query_result.matches]
            
            # Delete the vectors
            index.delete(ids=ids_to_delete)
            
            logging.info(f"Deleted {len(ids_to_delete)} vectors for document {doc_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to delete document: {str(e)}")
            raise
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the vector store"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            index = self.pc.Index(current_app.config['PINECONE_INDEX_NAME'])
            
            # Get stats to understand the data
            stats = index.describe_index_stats()
            
            # Query for a sample of documents to get metadata
            query_result = index.query(
                vector=[0.0] * 1536,  # Dummy vector
                top_k=100,
                include_metadata=True
            )
            
            # Group by document ID
            documents = {}
            for match in query_result.matches:
                if 'doc_id' in match.metadata:
                    doc_id = match.metadata['doc_id']
                    if doc_id not in documents:
                        documents[doc_id] = {
                            'doc_id': doc_id,
                            'filename': match.metadata.get('filename', 'Unknown'),
                            'upload_time': match.metadata.get('upload_time', 'Unknown'),
                            'chunk_count': 0
                        }
                    documents[doc_id]['chunk_count'] += 1
            
            return list(documents.values())
            
        except Exception as e:
            logging.error(f"Failed to list documents: {str(e)}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")
            
            index = self.pc.Index(current_app.config['PINECONE_INDEX_NAME'])
            stats = index.describe_index_stats()
            
            return {
                'total_vectors': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness,
                'namespaces': dict(stats.namespaces) if stats.namespaces else {}
            }
            
        except Exception as e:
            logging.error(f"Failed to get stats: {str(e)}")
            raise
