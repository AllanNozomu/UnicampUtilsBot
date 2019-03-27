# -*- coding: utf-8 -*-
import unittest
import os

from settings import settings

class TestSettings(unittest.TestCase):

    def test_getenv_TELEGRAM_BOT_TOKEN(self):
        BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", None)
        self.assertIsNotNone(BOT_TOKEN)

    def test_settings_BOT_TOKEN(self):
        self.assertIsNotNone(settings.BOT_TOKEN)

if __name__ == '__main__':
    unittest.main()