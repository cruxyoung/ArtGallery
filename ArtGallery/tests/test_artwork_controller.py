from django.test import Client
from django.test import TestCase
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from datetime import datetime
from ArtGallery import models
from ArtGallery.controllers import artwork_controller


class TestArtwork(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = models.User.objects.create(username='ink',
                                                password='123233',
                                                first_name='Micheal',
                                                last_name='Jordan',
                                                email='nikelazy@gmail.com',
                                                is_staff=1,
                                                is_active=1,
                                                date_joined='2017-10-27',
                                                last_login='2017-10-27')
        self.user2 = models.User.objects.create(username='ink2',
                                                password='123233',
                                                first_name='Micheal',
                                                last_name='Jordan',
                                                email='nikelazy@gmail.com',
                                                is_staff=0,
                                                is_active=1,
                                                date_joined='2017-10-27',
                                                last_login='2017-10-27')
        user1 = models.User.objects.get(username='ink')
        user2 = models.User.objects.get(username='ink2')
        models.UserProfile.objects.create(sex=1, amount=0, identity=0, user_id=user1)
        models.UserProfile.objects.create(sex=1, amount=0, identity=1, user_id=user2)
        models.ArtWork.objects.create(aw_name='test1',
                                      aw_location='China',
                                      aw_type='Abstract',
                                      aw_genre='Normal Painting',
                                      aw_auctionStat=0,
                                      aw_description='test_description',
                                      aw_img='artwork/1509014721.720959/Art_au_b0.jpg',
                                      artist_id=user1,
                                      aw_time=datetime.now(),
                                      aw_totalAward=0.0)
        models.ArtWork.objects.create(aw_name='test2',
                                      aw_location='China',
                                      aw_type='Abstract',
                                      aw_genre='Normal Painting',
                                      aw_auctionStat=0,
                                      aw_description='test_description',
                                      aw_img='artwork/1509014721.720959/Art_au_b0.jpg',
                                      artist_id=user1,
                                      aw_time=datetime.now(),
                                      aw_totalAward=0.0)
        artwork = models.ArtWork.objects.get(aw_name='test2')
        models.AuctionRecord.objects.create(ar_originalPrice=100,
                                            ar_time='2017-10-10',
                                            ar_end_time='2017-11-11',
                                            ar_finalPrice=200,
                                            aw_id=artwork)

    def test_artwork_details(self):
        request = self.factory.get('/artworks/1/details')
        request.user = self.user1

        response = artwork_controller.artwork_detail(request, 1)
        self.assertEqual(response.status_code, 200)
        data = {"favouriteButton": "Favorite"}
        response2 = self.client.post('/artworks/2/detail', data)

        self.assertEqual(response2.status_code, 301)
