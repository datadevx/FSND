from datetime import datetime, timedelta
import unittest
import json
import requests
from app import create_app, db
from app.models import Gender, Actor, Movie
from app.date import now


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Gender.insert_genders()
        self.client = self.app.test_client()
        self.endpoints = {
            'actors': f'/api/{self.app.config["THECREW_API_VERSION"]}/actors',
            'movies': f'/api/{self.app.config["THECREW_API_VERSION"]}/movies'
        }
        self.token = {}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        if not self.token or (
                self.token
                and now() + timedelta(seconds=self.token['expires_in']) <
                now() + timedelta(seconds=60)):
            url = f'https://{self.app.config["THECREW_AUTH0_DOMAIN"]}/oauth/token'
            payload = {
                'client_id': 'nHaRDZC2Ro6Qvo2bnj58WmukR2UDHd4b',
                'client_secret':
                'n4ft7fYUgdJIEg0CX1O2VERnaFq2F46NmwAjmNcEV6jyo5Wiz68s0TV7piNYjJCg',
                'audience': 'thecrew-api',
                'grant_type': 'client_credentials'
            }
            response = requests.post(url, json=payload)
            self.token = response.json()

        bearer_token = f'{self.token["token_type"]} {self.token["access_token"]}'
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': bearer_token
        }

    def test_crud_actors(self):
        # add a actor
        response = self.client.post(self.endpoints['actors'],
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'age':
                                        23,
                                        'gender':
                                        'Female',
                                        'fullName':
                                        'Sanjana Sanghi'
                                    }))
        self.assertEqual(response.status_code, 201)
        url_actor = response.headers.get('Location')
        self.assertIsNotNone(url_actor)

        movie = Movie(
            title='Dil Bechara',
            release_date=datetime(2020, 7, 24),
            actors=[Actor.query.filter_by(full_name='Sanjana Sanghi').first()])
        db.session.add(movie)
        db.session.commit()

        # get the new actor
        response = self.client.get(url_actor, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['age'], 23)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 1)
        json_actor = json_response

        # get actors
        response = self.client.get(self.endpoints['actors'],
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0], json_actor)

        # update actor
        response = self.client.patch(url_actor,
                                     headers=self.get_api_headers(),
                                     data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_actor['uuid'])
        self.assertEqual(json_response['age'], 24)
        self.assertEqual(json_response['fullName'], 'Sanjana Sanghi')
        self.assertEqual(json_response['gender'], 'Female')
        self.assertEqual(json_response['moviesCount'], 1)

        # delete actor
        response = self.client.delete(url_actor,
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

    def test_methods_not_allowed_for_actors(self):
        response = self.client.post(self.endpoints['actors'],
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'age':
                                        23,
                                        'gender':
                                        'Female',
                                        'fullName':
                                        'Sanjana Sanghi'
                                    }))
        url_actor = response.headers.get('Location')

        # put not allowed
        response = self.client.put(self.endpoints['actors'],
                                   headers=self.get_api_headers(),
                                   data=json.dumps({
                                       'age': 23,
                                       'gender': 'Female',
                                       'fullName': 'Sanjana Sanghi'
                                   }))
        self.assertEqual(405, response.status_code)

        response = self.client.put(url_actor,
                                   headers=self.get_api_headers(),
                                   data=json.dumps({
                                       'age': 23,
                                       'gender': 'Female',
                                       'fullName': 'Sanjana Sanghi'
                                   }))
        self.assertEqual(405, response.status_code)

        # post/<uuid> not allowed
        response = self.client.post(url_actor,
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'age':
                                        23,
                                        'gender':
                                        'Female',
                                        'fullName':
                                        'Sanjana Sanghi'
                                    }))
        self.assertEqual(405, response.status_code)

        # patch all not allowed
        response = self.client.patch(self.endpoints['actors'],
                                     headers=self.get_api_headers(),
                                     data=json.dumps({'age': 24}))
        self.assertEqual(405, response.status_code)

        # delete all not allowed
        response = self.client.patch(self.endpoints['actors'],
                                     headers=self.get_api_headers())
        self.assertEqual(405, response.status_code)

    def add_actor(self):
        actor = Actor(age=23,
                      full_name='Sanjana Sanghi',
                      gender=Gender.query.filter_by(name='Female').first())
        db.session.add(actor)
        db.session.commit()
        return actor

    def test_cannot_get_actor_with_int_id(self):
        self.add_actor()

        response = self.client.get(self.endpoints['actors'] + '/1',
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_patch_actor_with_int_id(self):
        self.add_actor()

        response = self.client.patch(self.endpoints['actors'] + '/1',
                                     headers=self.get_api_headers(),
                                     data=json.dumps({'age': 24}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_delete_actor_with_int_id(self):
        self.add_actor()

        response = self.client.delete(self.endpoints['actors'] + '/1',
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_crud_movies(self):
        # add a movie
        actors = [
            Actor(age=23,
                  full_name='Sanjana Sanghi',
                  gender=Gender.query.filter_by(name='Female').first()),
            Actor(age=49,
                  full_name='Saswata Chatterjee',
                  gender=Gender.query.filter_by(name='Male').first()),
            Actor(age=49,
                  full_name='Saif Ali Khan',
                  gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(self.endpoints['movies'],
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'title':
                                        'Dil Bechara',
                                        'releaseDate':
                                        '2020-07-24',
                                        'actors':
                                        [a.to_json() for a in actors]
                                    }))
        self.assertEqual(response.status_code, 201)
        url_movie = response.headers.get('Location')
        self.assertIsNotNone(url_movie)

        # get the new movie
        response = self.client.get(url_movie, headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertTrue(json_response['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-24')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(json_response['actors'],
                             [a.to_json() for a in actors])
        json_movie = json_response

        # get movies
        response = self.client.get(self.endpoints['movies'],
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertIsNotNone(json_response['objects'])
        self.assertEqual(json_response.get('totalCount', 0), 1)
        self.assertEqual(json_response.get('totalPages', 0), 1)
        self.assertEqual(json_response.get('page', 0), 1)
        self.assertEqual(json_response['objects'][0], json_movie)

        # update movie
        response = self.client.patch(url_movie,
                                     headers=self.get_api_headers(),
                                     data=json.dumps(
                                         {'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json
        self.assertEqual(json_response['uuid'], json_movie['uuid'])
        self.assertEqual(json_response['title'], 'Dil Bechara')
        self.assertEqual(json_response['releaseDate'], '2020-07-31')
        self.assertEqual(len(json_response['actors']), 3)
        self.assertListEqual(json_response['actors'],
                             [a.to_json() for a in actors])

        # delete movie
        response = self.client.delete(url_movie,
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 204)

    def test_methods_not_allowed_for_movies(self):
        actors = [
            Actor(age=23,
                  full_name='Sanjana Sanghi',
                  gender=Gender.query.filter_by(name='Female').first()),
            Actor(age=49,
                  full_name='Saswata Chatterjee',
                  gender=Gender.query.filter_by(name='Male').first()),
            Actor(age=49,
                  full_name='Saif Ali Khan',
                  gender=Gender.query.filter_by(name='Male').first())
        ]
        db.session.add_all(actors)
        db.session.commit()

        response = self.client.post(self.endpoints['movies'],
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'title':
                                        'Dil Bechara',
                                        'releaseDate':
                                        '2020-07-24',
                                        'actors':
                                        [a.to_json() for a in actors]
                                    }))
        url_movie = response.headers.get('Location')

        # put not allowed
        response = self.client.put(self.endpoints['movies'],
                                   headers=self.get_api_headers(),
                                   data=json.dumps({
                                       'title':
                                       'Dil Bechara',
                                       'releaseDate':
                                       '2020-07-24',
                                       'actors': [a.to_json() for a in actors]
                                   }))
        self.assertEqual(405, response.status_code)

        response = self.client.put(url_movie,
                                   headers=self.get_api_headers(),
                                   data=json.dumps({
                                       'title':
                                       'Dil Bechara',
                                       'releaseDate':
                                       '2020-07-24',
                                       'actors': [a.to_json() for a in actors]
                                   }))
        self.assertEqual(405, response.status_code)

        # post/<uuid> not allowed
        response = self.client.post(url_movie,
                                    headers=self.get_api_headers(),
                                    data=json.dumps({
                                        'title':
                                        'Dil Bechara',
                                        'releaseDate':
                                        '2020-07-24',
                                        'actors':
                                        [a.to_json() for a in actors]
                                    }))
        self.assertEqual(405, response.status_code)

        # patch all not allowed
        response = self.client.patch(self.endpoints['movies'],
                                     headers=self.get_api_headers(),
                                     data=json.dumps(
                                         {'releaseDate': '2020-07-31'}))
        self.assertEqual(405, response.status_code)

        # delete all not allowed
        response = self.client.delete(self.endpoints['movies'],
                                      headers=self.get_api_headers())
        self.assertEqual(405, response.status_code)

    def add_movie(self):
        actor = Actor(age=23,
                      full_name='Sanjana Sanghi',
                      gender=Gender.query.filter_by(name='Female').first())
        db.session.add(actor)
        db.session.commit()

        movie = Movie(title='Dil Bechara',
                      release_date=datetime(2020, 7, 24),
                      actors=[actor])
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_cannot_get_movie_with_int_id(self):
        self.add_movie()

        response = self.client.get(self.endpoints['movies'] + '/1',
                                   headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_patch_movie_with_int_id(self):
        self.add_movie()

        response = self.client.patch(self.endpoints['movies'] + '/1',
                                     headers=self.get_api_headers(),
                                     data=json.dumps(
                                         {'releaseDate': '2020-07-31'}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_delete_movie_with_int_id(self):
        self.add_movie()

        response = self.client.delete(self.endpoints['movies'] + '/1',
                                      headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(response.json)
        self.assertIsNotNone(response.json['message'])

    def test_cannot_post_movie_without_body(self):
        response = self.client.post(self.endpoints['movies'],
                                    headers=self.get_api_headers(),
                                    json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 3)
        self.assertListEqual(
            [e.get('code') for e in json_response.get('errors')],
            ['missing_field', 'missing_field', 'missing_field'])
        self.assertListEqual(
            sorted([e.get('field') for e in json_response.get('errors')]),
            ['actors', 'releaseDate', 'title'])

    def test_cannot_patch_movie_without_body(self):
        movie = self.add_movie()

        response = self.client.patch(
            f'{self.endpoints["movies"]}/{movie.uuid}',
            headers=self.get_api_headers(),
            json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 1)
        self.assertEqual(
            json_response.get('errors')[0]['code'], 'missing_field')
        self.assertIn('actors', json_response.get('errors')[0]['description'])
        self.assertIn('releaseDate',
                      json_response.get('errors')[0]['description'])
        self.assertIn('title', json_response.get('errors')[0]['description'])

    def test_cannot_post_actor_without_body(self):
        response = self.client.post(self.endpoints['actors'],
                                    headers=self.get_api_headers(),
                                    json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 3)
        self.assertListEqual(
            [e.get('code') for e in json_response.get('errors')],
            ['missing_field', 'missing_field', 'missing_field'])
        self.assertListEqual(
            sorted([e.get('field') for e in json_response.get('errors')]),
            ['age', 'fullName', 'gender'])

    def test_cannot_patch_actor_without_body(self):
        actor = self.add_actor()

        response = self.client.patch(
            f'{self.endpoints["actors"]}/{actor.uuid}',
            headers=self.get_api_headers(),
            json='')
        self.assertEqual(response.status_code, 400)
        json_response = response.json
        self.assertEqual(len(json_response.get('errors', 0)), 1)
        self.assertEqual(
            json_response.get('errors')[0]['code'], 'missing_field')
        self.assertIn('age', json_response.get('errors')[0]['description'])
        self.assertIn('fullName',
                      json_response.get('errors')[0]['description'])
        self.assertIn('gender', json_response.get('errors')[0]['description'])
