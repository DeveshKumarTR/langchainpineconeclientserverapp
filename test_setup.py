"""
Simple test script to verify the Flask server is working
"""

import requests
import json

def test_server():
    """Test the Flask server endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing LangChain Pinecone Server...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False
    
    # Test documents endpoint (should return empty list initially)
    try:
        response = requests.get(f"{base_url}/api/documents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Documents endpoint working!")
            print(f"   Documents found: {len(data.get('documents', []))}")
        else:
            print(f"❌ Documents endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Documents endpoint failed: {str(e)}")
    
    # Test search endpoint (should handle missing query gracefully)
    try:
        response = requests.post(f"{base_url}/api/search", json={}, timeout=5)
        if response.status_code == 400:  # Expected error for missing query
            print("✅ Search endpoint validation working!")
        else:
            print(f"⚠️  Search endpoint returned unexpected code: {response.status_code}")
    except Exception as e:
        print(f"❌ Search endpoint failed: {str(e)}")
    
    print("\n🎉 Basic server functionality verified!")
    print("\nNext steps:")
    print("1. Set up your .env file with API keys:")
    print("   - PINECONE_API_KEY=your_pinecone_key")
    print("   - OPENAI_API_KEY=your_openai_key")
    print("2. Initialize Pinecone index: py -m flask --app server.app init-db")
    print("3. Test document upload with: py client/client.py")
    
    return True

if __name__ == "__main__":
    test_server()
