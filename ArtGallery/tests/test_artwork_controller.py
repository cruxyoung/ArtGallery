from django.test import TestCase
from django.test import RequestFactory
from datetime import datetime
from ArtGallery import models
from ArtGallery.controllers import artwork_controller


class TestArtwork(TestCase):
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
                                                password='123233',
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
                                      aw_auctionStat=1,
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

    # For viewing the page and basic favorite function
    def test_artwork_details(self):
        request = self.factory.get('/artworks/2/detail')
        request.user = self.user1

        response = artwork_controller.artwork_detail(request, 2)
        self.assertEqual(response.status_code, 200)

        # test Favorite Function without favorite record
        data = {"favouriteButton": "Favorite"}

        response2 = self.client.post('/artworks/2/detail', data)

        self.assertEqual(response2.status_code, 301)

    def test_cancel_favorite(self):
        test_artwork = models.ArtWork.objects.get(aw_name='test2')
        models.FavoriteRecord.objects.create(fav_time=datetime.now(),
                                             artist_id=self.user2,
                                             aw_id=test_artwork)

        request = self.factory.get('/artworks/2/detail')
        request.user = self.user2
        # test Favorite Function with favorite record
        request.POST = {"favouriteButton": "Favorite"}
        artwork_controller.artwork_detail(request, 1)

    def test_artist_info(self):
        request = self.factory.get('/artists/1/detail')
        request.user = self.user1

        response = artwork_controller.artist_detail(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_ajax_reward(self):
        # Sufficient amount
        request = self.factory.get('/artists/1/detail')
        request.user = self.user2
        request.POST = {'reward_amount': 1.0}
        artwork_controller.ajax_reward(request, 1)

        # Insufficient amount
        user_profile = models.UserProfile.objects.get(user_id=request.user)
        user_profile.amount = 0.0
        user_profile.save()
        request.user = self.user2
        request.POST = {'reward_amount': 1.0}
        artwork_controller.ajax_reward(request, 1)

    def test_ajax_comment(self):
        # Valid Comment
        request = self.factory.get('/artists/1/detail')
        request.user = self.user2
        request.POST = {'comment_content': 'Good',
                        'rating': 4.0}

        artwork_controller.ajax_comment(request, 1)
        # Invalid: low_bound
        request.POST = {'comment_content': 'Good',
                        'rating': 0.0}
        artwork_controller.ajax_comment(request, 1)
        # Invalid: high_bound
        request.POST = {'comment_content': 'Good',
                        'rating': 6.0}
        artwork_controller.ajax_comment(request, 1)
        # Invalid: contain '\' etc
        request.POST = {'comment_content': 'Good\$',
                        'rating': 6.0}
        artwork_controller.ajax_comment(request, 1)

    def test_ajax_bid(self):
        request = self.factory.get('/artists/1/detail')
        request.user = self.user2
        request.POST = {'ah_amount': 101}

        artwork_controller.ajax_bid(request, 2)

        request.POST = {'ah_amount': 102}
        artwork_controller.ajax_bid(request, 2)
        # Invalid: Low_bound
        request.POST = {'ah_amount': 101}
        artwork_controller.ajax_bid(request, 2)

        request.POST = {'ah_amount': 103}
        artwork_controller.ajax_bid(request, 2)
        # Invalid: Out of chances
        request.POST = {'ah_amount': 104}
        artwork_controller.ajax_bid(request, 2)

    def test_complaint(self):
        request = self.factory.get('/artworks/complaints/edit/1')
        request.user = self.user2
        artwork_controller.complaints_edit(request, 1)

        # Complaint Action
        request.POST = {'complaint_content': 'COMPLAINTS',
                        'complaint_type': 'ILLEGAL'}
        artwork_controller.complaints_action(request, 1)

        # Invalid Input: Submit Again
        artwork_controller.complaints_action(request, 1)

        # Withdraw Complaint
        artwork_controller.withdraw_complaints(request, 1)
