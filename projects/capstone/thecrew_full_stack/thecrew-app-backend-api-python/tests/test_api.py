import unittest
import json
from app import create_app, db
from app.models import Gender, Actor


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

    def test_crud_actors(self):
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

    def test_crud_movies(self):
        # add a movie
        actors = [
            Actor(age=23, full_name='Sanjana Sanghi',
                  gender=Gender.query.filter_by(name='Female').first()),
            Actor(age=49, full_name='Saswata Chatterjee',
                  gender=Gender.query.filter_by(name='Male').first()),
            Actor(age=49, full_name='Saif Ali Khan',
                  gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(
            '/api/v1/movies',
            headers=self.get_api_headers(),
            data=json.dumps({
                'title': 'Dil Bechara', 'release_date': '2020-07-24',
                'actors': [a.to_json() for a in actors]}))
        self.assertEqual(response.status_code, 201)
        url_movie = response.headers.get('Location')
        self.assertIsNotNone(url_movie)

        # get the new movie
        response = self.client.get(
            url_movie,
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['release_date'], '2020-07-24')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(json_response['actors'],
                             [a.to_json() for a in actors])
        json_movie = json_response

        # get movies
        response = self.client.get(
            '/api/v1/movies',
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0], json_movie)

        # edit movie
        response = self.client.patch(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps({'release_date': '2020-07-31'}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_movie['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['release_date'], '2020-07-31')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(json_response['actors'],
                             [a.to_json() for a in actors])

        # delete movie
        response = self.client.delete(
            url_movie,
            headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

        # put not allowed
        response = self.client.put(
            '/api/v1/movies',
            headers=self.get_api_headers(),
            data=json.dumps({
                'title': 'Dil Bechara', 'release_date': '2020-07-24',
                'actors': [a.to_json() for a in actors]}))
        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json)

        response = self.client.put(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps({
                'title': 'Dil Bechara', 'release_date': '2020-07-24',
                'actors': [a.to_json() for a in actors]}))
        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json)

        # post/<uuid> not allowed
        response = self.client.post(
            url_movie,
            headers=self.get_api_headers(),
            data=json.dumps({
                'title': 'Dil Bechara', 'release_date': '2020-07-24',
                'actors': [a.to_json() for a in actors]}))
        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json)

        # patch all not allowed
        response = self.client.patch(
            '/api/v1/movies',
            headers=self.get_api_headers(),
            data=json.dumps({'release_date': '2020-07-31'}))
        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json)

        # delete all not allowed
        response = self.client.patch(
            '/api/v1/movies',
            headers=self.get_api_headers(),
            data=json.dumps({'release_date': '2020-07-31'}))
        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json)
