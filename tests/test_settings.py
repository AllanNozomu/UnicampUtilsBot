# -*- coding: utf-8 -*-
import unittest
import os
from src.server import prepare_env

class TestSettings(unittest.TestCase):

    def setUp(self):
        prepare_env()

    def test_env(self):
        BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", None)
        self.assertIsNotNone(BOT_TOKEN)

if __name__ == '__main__':
    unittest.main()