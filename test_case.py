from fastapi.testclient import TestClient
from Huffman_Imcr import app
import json

client = TestClient(app)

payload = {"image_path": "sample1.jpg"}

response = client.post("/compress_image/", json=payload)
output = response.json()
print(output)

def test_response_code():
    assert response.status_code == 200

def test_validity():
    assert len(output)>2