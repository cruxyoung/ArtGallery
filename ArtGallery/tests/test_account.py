from django.test import Client
from django.test import TestCase
from ArtGallery import models


class TestAccountController(TestCase):
    def setUp(self):
        user = models.User.objects.create(username='ink', password='123233', first_name='micheal', last_name='jack',
                                   email='382742544@qq.com', is_active=1)
        models.UserProfile.objects.create(sex=1, amount=0, identity=1, user_id=user)

    def tearDown(self):
        pass

    def test_login(self):
        c = Client()

        response = c.post('/accounts/login', data=dict(username='ink', password='123233'), follow_redirects=True)
        self.assertEqual(301, response.status_code)

    #
    # def test_signup(self):
    #     c = Client()
    #     response =
    #
    def test_signup(self):
        response = self.client.post('/accounts/signup', data=dict(
            username='czlw',
            first_name='zhilinwei',
            last_name='chen',
            email='382742544@qq.com',
            password='123233',
            sex=False,
            identity=True,
            birthday='1993-11-11',
            amount=0
        ), follow_redirects=True)
        self.assertEqual(301, response.status_code)
