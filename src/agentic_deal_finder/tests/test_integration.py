import time
import multiprocessing
import uvicorn
import pytest
import httpx
from agentic_deal_finder.server import app 

# Configuration for the test server
HOST = "127.0.0.1"
PORT = 8005
BASE_URL = f"http://{HOST}:{PORT}"

def run_server():
    """Function to start the Uvicorn server."""
    uvicorn.run(app, host=HOST, port=PORT, log_level="error")

@pytest.fixture(scope="module", autouse=True)
def setup_server():
    """Starts the server before tests and shuts it down after."""
    proc = multiprocessing.Process(target=run_server, daemon=True)
    proc.start()
    
    # Give the server a moment to start up
    timeout = 5
    start_time = time.time()
    while True:
        try:
            with httpx.Client() as client:
                if client.get(f"{BASE_URL}/health").status_code == 200:
                    break
        except Exception:
            if time.time() - start_time > timeout:
                raise RuntimeError("Test server failed to start")
            time.sleep(0.1)
            
    yield
    proc.terminate()

class TestDealFinderIntegration:
    """Integration tests hitting the live running server."""

    def test_health_check(self):
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    def test_standard_search_integration(self):
        payload = {"query": "gaming mouse"}
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/search/standard", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "deals" in data
            assert data["source"] == "standard"

    def test_workflow_endpoint_integration(self):
        payload = {"query": "cheap headphones"}
        with httpx.Client() as client:
            # Setting a longer timeout as workflow logic can be slow
            response = client.post(f"{BASE_URL}/workflow", json=payload, timeout=30.0)
            assert response.status_code == 200
            assert "report_path" in response.json()