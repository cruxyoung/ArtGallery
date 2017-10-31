from django.test import Client
from django.test import TestCase
from ArtGallery import models
from django.core.urlresolvers import reverse
from datetime import datetime


class TestAccountController(TestCase):
    def setUp(self):
        models.User.objects.create(username="elec",
                                   password="123233",
                                   first_name="Micheal",
                                   last_name="Jordan",
                                   email="nikelazy@gmail.com",
                                   is_active=1,
                                   date_joined="2017-10-27",
                                   last_login="2017-10-27")
        user = models.User.objects.get(username="elec")
        models.UserProfile.objects.create(sex=1, amount=0, identity=1, user_id=user)

    def test_login(self):
        c = Client()
        data = {'username': 'elec',
                'password': '123233'}
        response = c.post('/accounts/login', data, follow_redirects=True)
        self.assertEqual(301, response.status_code)

    def test_signup(self):
        data = {
            'username': 'czlw',
            'first_name': 'zhilinwei',
            'last_name': 'chen',
            'email': '382742544@qq.com',
            'password1': 'elec123233',
            'password2': 'elec123233',
            'sex': False,
            'identity': True,
            'birthday': '1999-11-11',
        }
        response = self.client.post(reverse('signup'), data)

        self.assertEqual(200, response.status_code)

        data2 = {
            'username': 'elec',
            'first_name': 'zhilinwei',
            'last_name': 'chen',
            'email': '382742544@qq.com',
            'password1': 'elec123233',
            'password2': 'elec123233',
            'sex': False,
            'identity': False,
            'birthday': '1999-11-11',
        }
        response2 = self.client.post(reverse('signup'), data2)

        self.assertEqual(200, response2.status_code)
