from django.test import TestCase
from django.test import RequestFactory
from ArtGallery import models
from ArtGallery.controllers import personal_controller
from django.core.urlresolvers import reverse


class TestCustomerPersonalCenter(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = models.User.objects.create(username='elec',
                                                password='123233',
                                                first_name='Micheal',
                                                last_name='Jordan',
                                                email='nikelazy@gmail.com',
                                                is_staff=1,
                                                is_active=1,
                                                date_joined='2017-10-27',
                                                last_login='2017-10-27')
        self.user2 = models.User.objects.create(username='elec2',
                                                password='abc123233',
                                                first_name='Micheal',
                                                last_name='Jordan',
                                                email='nikelazy@gmail.com',
                                                is_staff=0,
                                                is_active=1,
                                                date_joined='2017-10-27',
                                                last_login='2017-10-27')
        # user1 is artist, user2 is customer
        user1 = models.User.objects.get(username='elec')
        user2 = models.User.objects.get(username='elec2')
        models.UserProfile.objects.create(sex=1, amount=0, identity=0, user_id=user1)
        models.UserProfile.objects.create(sex=1, amount=100, identity=1, user_id=user2)

    def test_personal_favorite(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 200)

        # Sort by time
        response = self.client.get(reverse('favorite'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

    def test_personal_auction(self):
        response = self.client.get(reverse('customer_auction'))
        self.assertEqual(response.status_code, 200)

        # Sort by Time or Price
        response = self.client.get(reverse('customer_auction'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('customer_auction'), {'sort': 'price'})
        self.assertEqual(response.status_code, 200)

    def test_personal_reward(self):
        response = self.client.get(reverse('customer_reward'))
        self.assertEqual(response.status_code, 200)

        # Sort by Time or Price
        response = self.client.get(reverse('customer_reward'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('customer_reward'), {'sort': 'price'})
        self.assertEqual(response.status_code, 200)

    def test_personal_comment(self):
        response = self.client.get(reverse('customer_comment'))
        self.assertEqual(response.status_code, 200)

        # Sort by Time
        response = self.client.get(reverse('customer_comment'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

        # Sort by Time
        response = self.client.get(reverse('customer_comment'), {'sort': 'reply'})
        self.assertEqual(response.status_code, 200)

    def test_personal_complaint(self):
        response = self.client.get(reverse('customer_complaint'))
        self.assertEqual(response.status_code, 200)

    def test_personal_setting(self):
        request = self.factory.get('/customer/settings/')
        request.user = self.user2
        response = personal_controller.PersonalSetting.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_personal_setting_change_pwd(self):
        request = self.factory.post('/customer/settings/')
        request.user = self.user2
        request.POST = {'password1': 'abc123233',
                        'password2': 'elec123233',
                        'password3': 'elec123233'}
        response = personal_controller.PersonalSetting.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # Invalid input: contain invalid characters
        request.POST = {'password1': '123233',
                        'password2': 'elec123233<',
                        'password3': 'elec123233<'}
        response = personal_controller.PersonalSetting.as_view()(request)

        self.assertEqual(response.status_code, 200)
        # Invalid input: did not match origin pwd
        request.POST = {'password1': '1232',
                        'password2': 'elec123233<',
                        'password3': 'elec123233<'}
        response = personal_controller.PersonalSetting.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # Successful
        request.POST = {'password1': 'elec123233',
                        'password2': 'eeee123456',
                        'password3': 'eeee123456'}
        response = personal_controller.PersonalSetting.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_edit_user_info(self):
        request = self.factory.post('/user/settings/edit_info/')
        request.user = self.user2
        request.POST = {'username': 'elec',
                        'first_name': 'ELEC',
                        'last_name': 'Hello9609',
                        'email': 'elec9609@uni.sydney.edu.au'}
        response = personal_controller.UserInfoView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Invalid input: contain invalid characters
        request.POST = {'username': 'elec',
                        'first_name': 'ELEC',
                        'last_name': 'Hello9609<<',
                        'email': 'elec9609@uni.sydney.edu.au'}
        response = personal_controller.UserInfoView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_deposit_money(self):
        request = self.factory.post('/user/settings/deposit_money/')
        request.user = self.user2
        request.POST = {'money': 100}
        response = personal_controller.DepositMoney.as_view()(request)
        self.assertEqual(response.status_code, 200)
