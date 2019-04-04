import unittest

from async import login
from utils.helpers import s3fs, paths
from utils.selenium import get_driver


class TestLogin(unittest.TestCase):

    def test_login(self):
        if s3fs.exists(f'{paths["cookies"]}/'):
            s3fs.removetree(f'{paths["cookies"]}')
        self.driver = get_driver()
        login.enter_notion(self.driver)
