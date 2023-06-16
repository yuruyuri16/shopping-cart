import unittest
from unittest.mock import MagicMock, Mock
from sqlalchemy.orm import Session
import schemas
from fastapi import status

import models
from crud import (get_products, create_cart_product,
                  update_product, get_product, delete_product, get_cart, get_carts, create_cart)


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_get_products(self):
        products = [models.Product(id=1, title="Product 1"), models.Product(
            id=2, title="Product 2")]
        self.db.query.return_value.offset.return_value.limit.return_value.all.return_value = products

        result = get_products(self.db, skip=0, limit=10)

        self.assertEqual(result, products)

    def test_create_cart_product(self):
        product = schemas.ProductCreate(
            title='testtitle', price=0, description='', category='', image='', rating='')
        cart_id = 1

        result = create_cart_product(self.db, product, cart_id)

        self.assertEqual(result.owner_id, cart_id)
        self.assertEqual(result.title, product.title)
        self.assertEqual(result.price, product.price)
        self.assertEqual(result.description, product.description)
        self.assertEqual(result.category, product.category)
        self.assertEqual(result.image, product.image)
        self.assertEqual(result.rating, product.rating)

    def test_update_product(self):
        product_id = 1
        updated_product = schemas.UpdateProduct(id=0,
                                                title='testtitle', price=0, description='', category='', image='', rating='')

        existing_product = models.Product(id=1, price=0)
        self.db.query.return_value.filter.return_value.first.return_value = existing_product

        result = update_product(product_id, updated_product, self.db)

        self.assertEqual(result.id, product_id)
        self.assertEqual(result.price, updated_product.price)

    def test_get_product(self):
        product_id = 1

        product = models.Product(id=1, title="Product 1")
        self.db.query.return_value.filter.return_value.first.return_value = product

        result = get_product(self.db, product_id)

        self.assertEqual(result, product)

    def test_delete_product(self):
        product_id = 1

        existing_product = models.Product(id=1, title="Product 1")
        self.db.query.return_value.filter.return_value.first.return_value = existing_product

        result = delete_product(product_id, self.db)

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_cart(self):
        cart_id = 1

        cart = models.Cart()
        self.db.query.return_value.filter.return_value.first.return_value = cart

        result = get_cart(self.db, cart_id)

        self.assertEqual(result, cart)

    def test_get_carts(self):
        carts = [models.Cart(), models.Cart()]
        self.db.query.return_value.offset.return_value.limit.return_value.all.return_value = carts

        result = get_carts(self.db, skip=0, limit=10)

        self.assertEqual(result, carts)

    def test_create_cart(self):
        cart_data = schemas.CartCreate(id=0)

        result = create_cart(self.db, cart_data)

        self.assertEqual(result.id, cart_data.id)


if __name__ == "__main__":
    unittest.main()
