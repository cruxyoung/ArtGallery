from django.test import TestCase
from django.test import RequestFactory
from ArtGallery import models
from ArtGallery.controllers import personal_artist_controller
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


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
        user = models.User.objects.get(username="elec")
        models.ArtWork.objects.create(aw_name="test1",
                                      aw_location="China",
                                      aw_type="Abstract",
                                      aw_genre="Normal Painting",
                                      aw_auctionStat=0,
                                      aw_description="test_description",
                                      aw_img="artwork/1509014721.720959/Art_au_b0.jpg",
                                      artist_id=user,
                                      aw_time=datetime.now(),
                                      aw_totalAward=0.0)
        models.ArtWork.objects.create(aw_name="test2",
                                      aw_location="China",
                                      aw_type="Abstract",
                                      aw_genre="Normal Painting",
                                      aw_auctionStat=1,
                                      aw_description="test_description",
                                      aw_img="artwork/1509014721.720959/Art_au_b0.jpg",
                                      artist_id=user,
                                      aw_time=datetime.now(),
                                      aw_totalAward=0.0)
        artwork = models.ArtWork.objects.get(aw_name='test2')
        models.AuctionRecord.objects.create(ar_originalPrice=100,
                                            ar_time='2017-10-10',
                                            ar_end_time='2017-11-11',
                                            ar_finalPrice=200,
                                            aw_id=artwork)
        # user1 is artist
        user1 = models.User.objects.get(username='elec')
        models.UserProfile.objects.create(sex=1, amount=0, identity=0, user_id=user1)

    def test_artwork_view(self):
        request = self.factory.get('/artist/artworks/')
        request.user = self.user1
        response = personal_artist_controller.ArtistArtwork.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Artwork Edit View
        request = self.factory.get('/artist/artworks/edit/1')
        request.user = self.user1
        response = personal_artist_controller.ArtworkEdit.as_view()(request, 1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get('/artist/artworks/edit/2')
        request.user = self.user1
        response = personal_artist_controller.ArtworkEdit.as_view()(request, 2)
        self.assertEqual(response.status_code, 200)

        # Artwork Edit View With Creating Operation
        request = self.factory.get('/artist/artworks/edit/0')
        request.user = self.user1
        response = personal_artist_controller.ArtworkEdit.as_view()(request, 0)
        self.assertEqual(response.status_code, 200)

    def test_edit_action(self):
        request = self.factory.post('/artist/artworks/edit/action/')
        request.user = self.user1

        from django.core.files.uploadedfile import File
        aw_img = File(open("static/img-default.png", 'rb'))
        request.FILES.update({'aw_img': aw_img})
        request.POST = {'aw_name': 'test3',
                        'aw_location': 'China',
                        'aw_type': 'Abstract',
                        'aw_genre': 'Normal Painting',
                        'aw_description': 'test_description'}
        response = personal_artist_controller.EditAction.as_view()(request)
        self.assertEqual(response.status_code, 200)

        aw_img = File(open("static/img-default.png", 'rb'))
        request.FILES.update({'aw_img': aw_img})
        request.POST = {'artwork_id': 1,
                        'aw_name': 'test3',
                        'aw_location': 'China',
                        'aw_type': 'Abstract',
                        'aw_genre': 'Normal Painting',
                        'aw_description': 'test_description'}
        response = personal_artist_controller.EditAction.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_delete_artwork(self):
        request = self.factory.get('/artist/artworks/delete/1')
        request.user = self.user1
        response = personal_artist_controller.delete_artwork(request, 1)
        self.assertEqual(response.status_code, 302)

    def test_artwork_auction(self):
        request = self.factory.get('/artist/artworks/edit/auction/')
        request.user = self.user1
        response = personal_artist_controller.ArtworkAuction.as_view()(request, 2)
        self.assertEqual(response.status_code, 200)

    def test_artwork_switch_auction(self):
        request = self.factory.post('/artist/artworks/edit/auction')
        request.user = self.user1
        request.POST = {'auctionStart': '2017-10-10T20:00',
                        'auctionEnd': '2017-10-10T20:00',
                        'ar_originalPrice': '50',
                        'aw_auction': '1'}

        response = personal_artist_controller.ArtworkAuction.as_view()(request, 2)
        self.assertEqual(response.status_code, 200)

    def test_artist_setting(self):
        request = self.factory.get('/artist/settings/')
        request.user = self.user1
        response = personal_artist_controller.ArtistSetting.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/artist/settings/')
        request.user = self.user1
        request.POST = {'password1': 'abc123233',
                        'password2': 'elec123233',
                        'password3': 'elec123233'}
        response = personal_artist_controller.ArtistSetting.as_view()(request)

        self.assertEqual(response.status_code, 200)
        request = self.factory.post('/artist/settings/')
        request.user = self.user1
        # Invalid input: contain invalid characters
        request.POST = {'password1': '123233',
                        'password2': 'elec123233<',
                        'password3': 'elec123233<'}
        response = personal_artist_controller.ArtistSetting.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Invalid input: error form
        request.POST = {'password1': '',
                        'password2': 'elec123233<',
                        'password3': 'elec123233<'}
        response = personal_artist_controller.ArtistSetting.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_artist_artwork_reward(self):
        request = self.factory.get('/artist/artworks/reward_history/1')
        request.user = self.user1
        response = personal_artist_controller.ArtworkReward.as_view()(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_artist_favorite(self):
        request = self.factory.get('artist/favorites/')
        request.user = self.user1
        response = personal_artist_controller.PersonalFavorite.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Sort By Time
        self.user = self.user1
        response = self.client.get(reverse('favorite'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

    def test_artist_comment(self):
        request = self.factory.get('/artist/comments/')
        request.user = self.user1
        response = personal_artist_controller.PersonalComment.as_view()(request)
        self.assertEqual(response.status_code, 200)

        # Sort By Time, Comment, Reply respectively
        self.user = self.user1
        response = self.client.get(reverse('artist_comment'), {'sort': 'time'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('artist_comment'), {'sort': 'comment'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('artist_comment'), {'sort': 'reply'})
        self.assertEqual(response.status_code, 200)
