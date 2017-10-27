from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse


class IndexViewTest(TestCase):
    def test_index_page(self):
        response = Client().get(reverse('index'))
        self.assertEqual(200, response.status_code)

# class PostSearchInfoTest(TestCase):
#     def setUp(self):
#         super(PostSearchInfoTest, self).setUp()
