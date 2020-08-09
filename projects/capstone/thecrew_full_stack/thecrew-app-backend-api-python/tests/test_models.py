import unittest
from datetime import datetime
from app import create_app, db
from app.models import Gender, Actor, Movie


class BaseModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class GenderCrudTestCase(BaseModelTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        self.assertEqual(len(Gender.query.all()), 3)
        self.assertEqual(Gender.query.filter_by(
            name='Female').first(), female)
        self.assertEqual(Gender.query.filter_by(
            name='Male').first(), male)
        self.assertEqual(Gender.query.filter_by(
            name='Another').first(), another)

        female.name = 'F'
        male.name = 'M'
        another.name = 'A'
        db.session.commit()

        self.assertEqual(Gender.query.filter_by(
            name='F').first(), female)
        self.assertEqual(Gender.query.filter_by(
            name='M').first(), male)
        self.assertEqual(Gender.query.filter_by(
            name='A').first(), another)

        db.session.delete(female)
        db.session.delete(male)
        db.session.delete(another)
        db.session.commit()

        self.assertFalse(Actor.query.all())


class ActorCrudTestCase(BaseModelTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        actress = Actor(
            age=23,
            full_name='Sanjana Sanghi',
            gender=female)

        actor1 = Actor(
            age=49,
            full_name='Saswata Chatterjee',
            gender=male)

        actor2 = Actor(
            age=50,
            full_name='Saif Ali Khan',
            gender=male)

        db.session.add_all([actress, actor1, actor2])
        db.session.commit()

        self.assertEqual(len(Actor.query.all()), 3)
        self.assertEqual(Actor.query.filter_by(
            full_name='Sanjana Sanghi').first(), actress)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saswata Chatterjee').first(), actor1)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saif Ali Khan').first(), actor2)

        self.assertEqual(Actor.query.filter_by(
            full_name='Sanjana Sanghi').first().full_name, 'Sanjana Sanghi')
        self.assertEqual(Actor.query.filter_by(
            full_name='Saswata Chatterjee').first().full_name, 'Saswata Chatterjee')
        self.assertEqual(Actor.query.filter_by(
            full_name='Saif Ali Khan').first().full_name, 'Saif Ali Khan')

        self.assertEqual(Actor.query.filter_by(
            full_name='Sanjana Sanghi').first().gender.name, 'Female')
        self.assertEqual(Actor.query.filter_by(
            full_name='Saswata Chatterjee').first().gender.name, 'Male')
        self.assertEqual(Actor.query.filter_by(
            full_name='Saif Ali Khan').first().gender.name, 'Male')

        self.assertEqual(Actor.query.filter_by(
            full_name='Sanjana Sanghi').first().age, 23)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saswata Chatterjee').first().age, 49)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saif Ali Khan').first().age, 50)

        actress.age = 24
        actor1.full_name = 'Saswata ChatterJ'
        actor2.gender = another
        db.session.commit()

        self.assertEqual(Actor.query.filter_by(
            full_name='Sanjana Sanghi').first().age, 24)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saswata ChatterJ').first(), actor1)
        self.assertEqual(Actor.query.filter_by(
            full_name='Saif Ali Khan').first().gender.name, 'Another')

        db.session.delete(actress)
        db.session.delete(actor1)
        db.session.delete(actor2)
        db.session.commit()

        self.assertFalse(Actor.query.all())


class MovieCrudTestCase(BaseModelTestCase):
    def test_crud(self):
        female = Gender(name='Female')
        male = Gender(name='Male')
        another = Gender(name='Another')
        db.session.add_all([female, male, another])
        db.session.commit()

        actress = Actor(
            age=23,
            full_name='Sanjana Sanghi',
            gender=female)

        actor1 = Actor(
            age=49,
            full_name='Saswata Chatterjee',
            gender=male)

        actor2 = Actor(
            age=49,
            full_name='Saif Ali Khan',
            gender=male)

        db.session.add_all([actress, actor1, actor2])
        db.session.commit()

        movie = Movie(
            title='Dil Bechara',
            release_date=datetime(2020, 7, 24),
            actors=[actress, actor1, actor2])
        db.session.add(movie)
        db.session.commit()

        self.assertEqual(len(Movie.query.all()), 1)
        self.assertEqual(Movie.query.filter_by(
            title='Dil Bechara').first(), movie)
        self.assertEqual(Movie.query.filter_by(
            title='Dil Bechara').first().release_date,
            datetime(2020, 7, 24).date())
        self.assertListEqual([a.full_name for a in Movie.query.filter_by(
            title='Dil Bechara').first().actors], [
                'Sanjana Sanghi', 'Saswata Chatterjee', 'Saif Ali Khan'])

        movie.release_date = datetime(2020, 7, 31)
        db.session.commit()

        self.assertEqual(Movie.query.filter_by(
            title='Dil Bechara').first().release_date,
            datetime(2020, 7, 31).date())

        db.session.delete(movie)
        db.session.commit()

        self.assertFalse(Movie.query.all())
