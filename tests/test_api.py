# Kod: Engelska
# Kommentarer: Svenska
# För att "unit testa" / sanity checks på mitt API med TestClient.
from fastapi.testclient import TestClient
from src.main import app


# Skapa en virtuell klient som pratar med min fastAPI app(main.py)
client = TestClient(app)

# Test 1 - Säkerställ med assert att response.json == "message" på root endpoint.
def test_root_endpoint():
    """Testing to make sure that root-endpoint answers and gives correct message"""
    response = client.get("/")
    assert response.status_code == 200
    # assert "Glossary API" in response.json()["message"] # Snällare test
    assert response.json() == {"message": "Welcome to my Glossary API. Use the /docs endpoint"} # Striktare test kräver EXAKT matchning!

# Test 2 - Säkerställ via assert att endpoint /health ger korrekt status.
def test_health_check_endpoint():
    """Testing to make sure that health-endpoint works and that DB is connected"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"} # Strikt test, kräver EXAKT matchning!
    # assert response.json()["status"] == "healthy" # Snällare test
    # assert response.json()["database"] == "connected" # Snällare test
    
