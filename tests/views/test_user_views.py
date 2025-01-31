def test_request_example(client):
    response = client.get("/signup")
    assert "<h1>サインアップ</h1>" in response.data.decode("utf-8")
