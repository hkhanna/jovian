def test_list_api(client, db):
    """The API returns the expected number of records"""
    expected = 1000
    response = client.get("/api/matches/")
    assert len(response.data) == expected
