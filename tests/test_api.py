def test_health_check_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_equilibrium_endpoint_returns_success(client):
    payload = {"matrix": [[10, 20], [15, 5]]}

    response = client.post("/equilibrium", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["equilibrium_found"] is True
    assert "seller_a_strategy" in data
    assert data["message"] == "Равновесие Нэша успешно рассчитано"


def test_optimize_endpoint_returns_optimal_price(client):
    payload = {"cost": 500, "min_margin_pct": 30, "max_price": 1200}

    response = client.post("/optimize", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "optimal"
    assert data["optimal_price"] == 1200.0


def test_equilibrium_pydanctic_validation_error(client):
    response = client.post("/equilibrium", json={"matrix": "invalid"})
    assert response.status_code == 422


def test_optimize_validation_error(client):
    response = client.post("/optimize", json={"cost": -100, "min_margin_pct": 10})
    assert response.status_code == 422
