def test_read_all_crystals_returns_empty_list(client):
    # Act
    response = client.get("/crystals")
    response_body = response.get_json()

    # Assert 
    assert response.status_code == 200 
    assert response_body == []

def test_get_one_book(client, two_saved_crystals):
    # Act
    response = client.get("/crystals/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id":2,
        "name":"quartz",
        "color":"white",
        "powers":"loveeeee"

    }

def test_create_one_book(client):
    # Act
    response = client.post("/crystals", json={
        "name":"dull crystal",
        "color":"gray",
        "powers":"this one steals color"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Crystal dull crystal has been born! Woot woot!"