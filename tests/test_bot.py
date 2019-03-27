# -*- coding: utf-8 -*-
import unittest
from unittest import mock
import os

from src.bot import get_url, get_url_prepare_download, get_url_download, ALLOWED_METHODS, send_message


class TestBot(unittest.TestCase):

    def test_get_url(self):
        BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.assertIsNotNone(BOT_TOKEN)
        for method in ALLOWED_METHODS:
            self.assertEqual(get_url(method), "https://api.telegram.org/bot{}/{}".format(BOT_TOKEN,method) )

    def test_get_url_fail(self):
        self.assertRaises(Exception, get_url, 'invalid')

    def test_get_url_prepare_download(self):
        BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.assertIsNotNone(BOT_TOKEN)
        self.assertEqual(get_url_prepare_download(), "https://api.telegram.org/bot{}/getFile".format(BOT_TOKEN) )

    def test_get_url_download(self):
        BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.assertIsNotNone(BOT_TOKEN)
        self.assertEqual(get_url_download('file'), "https://api.telegram.org/file/bot{}/file".format(BOT_TOKEN) )

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data ):
                self.json_data = json_data

            def json(self):
                return self.json_data

        BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        if args[0] == "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN) :
            return MockResponse({"ok": "true"})

        return MockResponse(None)

    @mock.patch('requests.post', side_effect=mocked_requests_get)
    def test_send_message(self, mock_get):
        json_data = send_message(10, 'mensagem')
        self.assertEqual(json_data, {"ok": "true"})

if __name__ == '__main__':
    unittest.main()