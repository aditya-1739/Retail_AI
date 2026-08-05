def test_unauthorized_endpoints(client):
    # Verify endpoints require OAuth2 Bearer Authentication
    assert client.post("/classify-product").status_code == 401
    assert client.post("/recognize-face").status_code == 401
    assert client.post("/analyze-review", json={"review": "good"}).status_code == 401
    assert client.post("/chat", json={"message": "hello"}).status_code == 401

def test_sentiment_analysis_authorized(client):
    # 1. Register and login to generate token
    register_payload = {
        "email": "user@example.com",
        "password": "securepassword",
        "full_name": "Standard User"
    }
    client.post("/auth/register", json=register_payload)
    
    login_payload = {
        "username": "user@example.com",
        "password": "securepassword"
    }
    login_response = client.post("/auth/login", data=login_payload)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Access Sentiment route
    review_text = "This dress is absolutely wonderful! I love the fit."
    response = client.post(
        "/analyze-review",
        json={"review": review_text},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["review"] == review_text
    assert data["sentiment"] in ["Positive", "Negative"]
