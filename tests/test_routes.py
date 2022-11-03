def test_get_all_planets_with_no_records(client):
    # act
    response = client.get("/planets")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client, one_planet):
    # act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body == {
        "name": "Earth",
        "description": "our home",
        "color": "blue-green",
        "id": 1
    }

def test_post_one_planet(client):
    # act
    response = client.post("/planets", json=({
            "name": "Mercury",
            "description": "closest to sun",
            "color": "grey"
    }))
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert response_body == "Planet Mercury is created"

def test_planet_not_found(client, one_planet):
    # act
    response = client.get("/planets/2")
    response_body = response.get_json()

    # assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 2 is not found"}
