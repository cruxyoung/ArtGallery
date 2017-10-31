from django.test import Client
from django.test import TestCase
from django.test import RequestFactory
from django.core.urlresolvers import reverse
from datetime import datetime
from ArtGallery import models


class IndexViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = models.User.objects.create(username="elec",
                                               password="123233",
                                               first_name="Micheal",
                                               last_name="Jordan",
                                               email="nikelazy@gmail.com",
                                               is_active=1,
                                               date_joined="2017-10-27",
                                               last_login="2017-10-27")
        user = models.User.objects.get(username="elec")
        models.UserProfile.objects.create(sex=1, amount=0, identity=1, user_id=user)
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

    def test_index_page(self):
        response = Client().get(reverse("index"))
        self.assertEqual(200, response.status_code)

    def test_search_page(self):
        data_dict = {"filter": "test",
                     "genre-form": "Normal Painting",
                     "period-form": "All"}
        response = self.client.post(reverse("art_list"), data_dict, HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)


class IndexViewTestMoreThan5Artworks(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = models.User.objects.create(username="elec",
                                               password="123233",
                                               first_name="Micheal",
                                               last_name="Jordan",
                                               email="nikelazy@gmail.com",
                                               is_active=1,
                                               date_joined="2017-10-27",
                                               last_login="2017-10-27")
        user = models.User.objects.get(username="elec")
        models.UserProfile.objects.create(sex=1, amount=0, identity=1, user_id=user)
        count = 0
        while count < 5:
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
            count += 1

    def test_index_page(self):
        response = Client().get(reverse("index"))
        self.assertEqual(200, response.status_code)
