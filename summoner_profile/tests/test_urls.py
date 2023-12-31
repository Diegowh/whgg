from django.test import SimpleTestCase
from django.urls import reverse, resolve
from summoner_profile.views import SummonerProfileView


class TestUrls(SimpleTestCase):

    def test_summoner_profile_url_resolves(self):
        url = reverse('summoner_profile', args=['test_server', 'test_name', 'test_tagline'])
        self.assertEquals(resolve(url).func.view_class, SummonerProfileView)