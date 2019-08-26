# -*- coding: utf-8 -*-

from .context import imgur_gif_reversal_bot_data

import os
import json
import unittest


class TestImgurInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../tests/sample-data/rising-gallery.json')
        )

    def setUp(self):
        filename = TestImgurInterface.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME
        with open(filename, 'r') as f:
            self.sample_rising_gallery_response = json.load(f)

    def test_strip_ids_from_gallery_response(self):
        actual = imgur_gif_reversal_bot_data.strip_ids_from_gallery_response(
                self.sample_rising_gallery_response)
        expected = [
            "zeDj2kN", "Rpbl2qJ", "hzgyVld", "CvleTCB", "7jASMTE", "UIXJpQK",
            "hkTN3ZR", "3uiJsmB", "dSsCy99", "TtcaD57", "b7eCiWs", "eyQJxFb",
            "j125wKC", "gvOLzyq", "uRRBJSr", "kSIbXHZ", "4oTZItj", "5qwsKPV",
            "PnV94ix", "QgbynAG", "2Y3Co0i", "WsLgAdJ", "e7neC3m", "nbJTRUf",
            "9k97C6x", "4YRIwrc", "f1RQXE9", "pDbwaYV", "xXuWCQs", "491bQNx",
            "gZH0snK", "pzG9mmw", "37CZOU1", "WlbqKf4", "5SvTsgM", "sKa0ojs",
            "cAcfQkI", "3Fq46jC", "N8IX0SE", "tS3i0Q0", "L3UDv5R", "6JVuVgy",
            "6WyJNg8", "Bu7bMKZ", "pHuNEW7", "ko6QZeT", "MZszpdy", "y3BBCrX",
            "ATd4zax", "XGE6WUp", "vqdm5vV", "kJkC42C", "8hFhx9b", "p9JDFCH",
            "SxOyyJX", "2MjYp9r", "o40U9Kr", "SRHRGu5", "6kX5eak", "ogwgKQZ",
        ]
        self.assertEqual(actual, expected)
