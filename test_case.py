from fastapi.testclient import TestClient
from convert_compress import app
import json

client = TestClient(app)

payload = {"image_path": "sample10.gif", "output_path": "output_sample10.jpg"}

response = client.post("/compress_and_convert_image/", json=payload)
output = response.json()
print(output)

def test_response_code():
    assert response.status_code == 200

def test_validity():
    assert len(output)>2