
# -*- coding: utf-8 -*-

from .context import ii

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
        filename = cls.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME
        with open(filename, 'r') as f:
            cls.sample_rising_gallery_response = json.load(f)

    def setUp(self):
        filename = TestImgurInterface.SAMPLE_RISING_GALLERY_RESPONSE_FILENAME
        with open(filename, 'r') as f:
            self.sample_rising_gallery_response = json.load(f)
        self.interface = ii.ImgurInterface()
    
    def test_class_and_instance_jsons_are_identical(self):
        self.assertEqual(TestImgurInterface.sample_rising_gallery_response,
                         self.sample_rising_gallery_response)
        for i in range (0, len(TestImgurInterface.sample_rising_gallery_response['data'])):
            self.assertEqual(TestImgurInterface.sample_rising_gallery_response['data'][i],
                            self.sample_rising_gallery_response['data'][i])

        should_be_gif_self = self.sample_rising_gallery_response['data'][13]
        should_be_gif = TestImgurInterface.sample_rising_gallery_response['data'][7]
        # this line fails
        self.assertEqual(should_be_gif, should_be_gif_self)

    def test_image_is_gif(self):
        should_be_gif_self = self.sample_rising_gallery_response['data'][13]
        should_be_gif = TestImgurInterface.sample_rising_gallery_response['data'][7]
        # this line passes
        self.assertEqual(should_be_gif, should_be_gif_self)
        # line 1368 in rising-gallery.json
        # checking title just as a sanity check: is this the post we actually
        # want to test? 
        self.assertEqual(should_be_gif['title'], 'Hungry Squirrel')
        self.assertTrue(self.interface.image_is_gif(
                            should_be_gif['images'][0]))

    def test_image_is_video(self):
        should_be_video_self = TestImgurInterface.sample_rising_gallery_response['data'][22]
        should_be_video = TestImgurInterface.sample_rising_gallery_response['data'][12]
        # line 2373 in rising-gallery.json
        self.assertEqual(should_be_video['title'], 'Holy Shit')
        self.assertTrue(self.interface.image_is_gif(
                            should_be_video['images'][0]))

    def test_filter_gifs(self):
        filtered = self.interface.filter_gifs_from_gallery_response(TestImgurInterface.sample_rising_gallery_response)
        assert True


if __name__ == '__main__':
    unittest.main()