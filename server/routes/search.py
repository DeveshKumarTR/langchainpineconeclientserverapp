from flask import Blueprint, request, jsonify, current_app
from server.models.vector_store import VectorStoreManager

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['POST'])
def search_documents():
    """Search documents using vector similarity"""
    try:
        # Get query from request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        k = data.get('k', 5)  # Number of results to return
        filter_metadata = data.get('filter', {})
        
        # Perform search
        vector_store = VectorStoreManager()
        results = vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter_metadata
        )
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity_score': float(score)
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results,
            'total_results': len(formatted_results)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error performing search: {str(e)}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@search_bp.route('/search/similar', methods=['POST'])
def find_similar_documents():
    """Find documents similar to a given document ID"""
    try:
        data = request.get_json()
        if not data or 'doc_id' not in data:
            return jsonify({'error': 'Document ID is required'}), 400
        
        doc_id = data['doc_id']
        k = data.get('k', 5)
        
        vector_store = VectorStoreManager()
        results = vector_store.find_similar_documents(doc_id, k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity_score': float(score)
            })
        
        return jsonify({
            'success': True,
            'reference_doc_id': doc_id,
            'similar_documents': formatted_results,
            'total_results': len(formatted_results)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error finding similar documents: {str(e)}")
        return jsonify({'error': f'Failed to find similar documents: {str(e)}'}), 500

@search_bp.route('/search/stats', methods=['GET'])
def get_search_stats():
    """Get statistics about the vector database"""
    try:
        vector_store = VectorStoreManager()
        stats = vector_store.get_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500
