from httpx import AsyncClient

async def test_add_category(ac: AsyncClient):
    response = await ac.post("/menu/category", json={
        "name": "category1",
        "is_publish": True
    })
    assert response.status_code == 200
async def test_add_topping(ac: AsyncClient):
    response = await ac.post("/menu/topping", json={
        "name": "topping1"
    })
    assert response.status_code == 200

# pytest -v -s tests/