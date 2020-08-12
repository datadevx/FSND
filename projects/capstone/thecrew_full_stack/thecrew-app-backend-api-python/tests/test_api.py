import unittest
import json
from app import create_app, db
from app.models import Gender


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Gender.insert_genders()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_actors(self):
        # add a actor
        response = self.client.post(
            '/api/v1/actors',
            headers=self.get_api_headers(),
            data=json.dumps({
                'age': 23, 'gender': 'Female',
                'full_name': 'Sanjana Sanghi'}))
        self.assertEqual(response.status_code, 201)
        url_actor = response.headers.get('Location')
        self.assertIsNotNone(url_actor)

        # get the new actor
        response = self.client.get(
            url_actor,
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['age'], 23)
        self.assertEqual(json_response['full_name'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        json_actor = json_response

        # get actors
        response = self.client.get(
            '/api/v1/actors',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['actors'])
        self.assertEqual(json_response.get('count', 0), 1)
        self.assertEqual(json_response['actors'][0], json_actor)

        # edit actor
        response = self.client.patch(
            url_actor,
            headers=self.get_api_headers(),
            data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_actor['uuid'])
        self.assertEqual(json_response['age'], 24)
        self.assertEqual(json_response['full_name'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')

        # delete actor
        response = self.client.delete(
            url_actor,
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

    def test_movies(self):
        pass
