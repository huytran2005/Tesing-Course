from uuid import uuid4

from models.category import Category
from models.menu_item import MenuItem


class TestRestaurantMenuListBVA:
    """BVA Tests for GET /restaurants/{id}/menus"""

    def test_restaurant_id_empty(self, client):
        response = client.get("/restaurants/%20/menus")
        assert response.status_code in {404, 422}

    def test_restaurant_id_valid_uuid(self, client, db, test_restaurant):
        category = Category(id=uuid4(), restaurant_id=test_restaurant.id, name="C")
        db.add(category)
        db.commit()

        menu = MenuItem(
            restaurant_id=test_restaurant.id,
            category_id=category.id,
            name="M1",
            price=1,
            is_available=True,
        )
        db.add(menu)
        db.commit()

        response = client.get(f"/restaurants/{test_restaurant.id}/menus")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_restaurant_id_invalid_uuid(self, client):
        response = client.get("/restaurants/invalid-uuid/menus")
        assert response.status_code == 422

    def test_restaurant_id_zero_uuid(self, client):
        response = client.get("/restaurants/00000000-0000-0000-0000-000000000000/menus")
        assert response.status_code in {404, 422}

    def test_restaurant_id_nonexistent(self, client):
        response = client.get("/restaurants/99999999-9999-9999-9999-999999999999/menus")
        assert response.status_code in {404, 422}

    def test_restaurant_id_missing(self, client):
        response = client.get("/restaurants/menus")
        assert response.status_code == 422
