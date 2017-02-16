import unittest
from pyilchimp.mailchimp_manager import *
# from hypothesis import given
# import hypothesis.strategies as st
import os
"""
This test suite needs http mocking to speed up and modularise tests.

Property based testing would be nice too but hard to find functions that are well
enough isolated from the API to actually send it properties and expect any
sensible behaviour
"""


class TestCampaignAll(unittest.TestCase):
    def setUp(self):
        self.mc_manager = MailchimpManager(os.environ['MC_APIKEY'], 'us3')

    def test_campaign_manager_all(self):
        campaigns = self.mc_manager.campaigns.all()
        self.assertIsInstance(campaigns, list)
        for item in campaigns:
            self.assertIsInstance(item, Campaign)

    def test_build_path(self):
        campaigns = self.mc_manager.campaigns.all()
        self.assertEqual(self.mc_manager.campaigns._build_path('campaigns/123'),
                         'https://us3.api.mailchimp.com/3.0/campaigns/123')
        for campaign in campaigns:
            path = self.mc_manager.campaigns._build_path(campaign)
            self.assertIn('us3.', path)
            self.assertIn(campaign.id, path)
            self.assertIn('campaigns', path)

    def test_str_repr(self):
        campaigns = self.mc_manager.campaigns.all()
        for campaign in campaigns:
            str_human = campaign.__str__(human=True)
            str_machine = str(campaign)
            str_repr = repr(campaign)
            self.assertNotIn(campaign.id, str_human)
            self.assertEqual('campaigns/{}'.format(campaign.id), str_machine)
            self.assertIn('<', str_repr)
            self.assertIn('>', str_repr)
            self.assertIn('Campaign:', str_repr)

    def test_filter(self):
        campaigns = self.mc_manager.campaigns.all()
        campaigns_short = self.mc_manager.campaigns.all(filters={'count': 5})
        self.assertEqual(len(campaigns), 10)
        self.assertEqual(len(campaigns_short), 5)
