import unittest

from async import commands
from async import login
from utils.selenium import get_driver


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        login.enter_notion(self.driver)

    def test_create_metrics_page(self):
        commands.create_metrics_page(self.driver, days_from_today=0)

    def test_create_planner_page(self):
        commands.create_planner_page(self.driver, days_from_today=0)

    def test_create_log_late(self):
        commands.create_log_late(self.driver, description='Late for the gym', severity='5 min')

    def test_create_log_screen_time(self):
        commands.create_log_screen_time(self.driver, time='1hr 11m')

    def test_set_metric_gym(self):
        commands.set_metric_gym(self.driver)

    def test_set_metric_read(self):
        commands.set_metric_read(self.driver)

    def test_set_metric_out_of_bed(self):
        commands.set_metric_out_of_bed(self.driver, '11am')

    def test_set_metric_productivity(self):
        commands.set_metric_productivity(self.driver, '3')

    def test_set_metric_happiness(self):
        commands.set_metric_happiness(self.driver, '🙂')
