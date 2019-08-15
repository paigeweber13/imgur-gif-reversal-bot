
# -*- coding: utf-8 -*-

from .context import reverse_gifs

import os
import json
import unittest

class TestImgurInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 
                         'sample-data/rising-gallery.json')
            )

    def setUp(self):
        filename = TestImgurInterface.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME
        with open(filename, 'r') as f:
            self.sample_rising_gallery_response = json.load(f)


    def test_image_is_gif(self):
        print(self.sample_rising_gallery_response)
        assert True

    def test_filter_gifs(self):
        assert True


if __name__ == '__main__':
    unittest.main()