# Kod: Engelska
# Kommentarer: Svenska
import requests


# Alla HTTP anrop mot FastAPI samlade på ett ställe.
# Om API't byter port eller URL ändrar jag bara API_BASE

API_BASE = "http://127.0.0.1:8000"


def health_check() -> bool:
    """Returnerar True om API't svarar på /health."""
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def ask(query: str) -> dict:
    """Skickar en fråga till /ask och returnerar {"answer": ..., "sources": [...]}"""
    r = requests.post(f"{API_BASE}/ask", json={"query": query}, timeout=30)
    r.raise_for_status()
    return r.json()


def search(query: str, k: int = 5) -> list[dict]:
    """Semantisk sökning mot /search. Returnerar lista med träffar."""
    r = requests.get(f"{API_BASE}/search", params={"q": query, "k": k}, timeout=10)
    r.raise_for_status()
    return r.json()["results"]


def get_terms(
    search: str | None = None,
    category: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """Hämtar termer från /terms med valfria filter."""
    params: dict = {"limit": limit}
    if search:
        params["search"] = search
    if category:
        params["category"] = category
    r = requests.get(f"{API_BASE}/terms", params=params, timeout=10)
    r.raise_for_status()
    return r.json()
