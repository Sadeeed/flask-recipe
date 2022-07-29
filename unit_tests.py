import json

from base_test import BaseTest
import unittest

from apps.main.models import Recipe


class TestHome(BaseTest):

    def test_login(self):
        with self.app() as client:
            response = client.post('/auth/signin', data=json.dumps({
                'email': 'sadeedw@gmail.com',
                'password': 'p3gasis8'
            }))
            self.assertEqual(response.status_code, 200)

    def test_index(self):
        with self.app() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_recipe(self):
        with self.app() as client:
            response = client.get('/recipe/cake')
            self.assertEqual(response.status_code, 200)

    def test_recipe_not_found(self):
        with self.app() as client:
            response = client.get('/recipe/404')
            self.assertEqual(response.status_code, 404)

    def test_rate_recipe(self):
        with self.app() as client:
            response = client.post('/rate/12', json={
                'rating': 5
            })
            self.assertEqual(response.status_code, 200)

    def test_edit_recipe(self):
        with self.app() as client:
            response = client.post('/recipe/edit/12', json={
                'name': 'cake12',
                'method': 'test method',
                'vegan': True,
                'ingredients': [
                    {'name': 'test ingredient'}
                ]
            })
            self.assertEqual(response.status_code, 200)

    def test_delete_recipe(self):
        with self.app() as client:
            response = client.get('/recipe/delete/40')
            self.assertEqual(response.status_code, 200)

    # API Tests

    def test_add_recipe(self):
        with self.app() as client:
            response = client.post('/api/recipes', json={
                'name': 'test recipe',
                'method': 'test method',
                'vegan': True,
                'ingredients': [
                    {'name': 'test ingredient'}
                ]
            })
            self.assertEqual(response.status_code, 201)

    def test_get_recipe(self):
        with self.app() as client:
            response = client.get('/api/recipe/12')
            self.assertEqual(response.status_code, 200)

    def test_recipe_list(self):
        with self.app() as client:
            response = client.get('/api/recipes')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
