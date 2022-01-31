def test_list_api(client, db):
    """The API returns the expected number of records"""
    count = 1000
    page_length = 100
    response = client.get("/api/matches/")

    assert "count" in response.data
    assert response.data["count"] == count

    assert "results" in response.data
    assert len(response.data["results"]) == page_length
