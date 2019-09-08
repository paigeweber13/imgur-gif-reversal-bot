# -*- coding: utf-8 -*-

from .context import gif_reverser

import cv2
import numpy as np
import os
import unittest

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_GIF_FILE = ROOT_DIR + '/sample-data/spock.gif'
TEST_MP4_NO_SOUND = ROOT_DIR + '/sample-data/bagged-kitty.mp4'
TEST_MP4_SOUND = ROOT_DIR + '/sample-data/monkey-car.mp4'

EXPECTED_MP4_NO_SOUND_REVERSED = ROOT_DIR + \
    '/sample-data/bagged-kitty-reversed.mp4'
EXPECTED_GIF_REVERSED = ROOT_DIR + \
    '/sample-data/spock-reversed.mp4'

OUTPUT_FILENAME = ROOT_DIR + '/reversed-tmp.mp4'


class TestGifReverser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reverser = gif_reverser.GifReverser()

    def test_reverse_gif_file(self):
        TestGifReverser.reverser.reverse_gif(TEST_GIF_FILE, OUTPUT_FILENAME)
        expected = cv2.VideoCapture(EXPECTED_GIF_REVERSED)
        actual = cv2.VideoCapture(OUTPUT_FILENAME)
        self.assertEqual(expected.get(cv2.CAP_PROP_FPS),
                         actual.get(cv2.CAP_PROP_FPS))
        expected_height, expected_width, expected_layers = expected.read()[
            1].shape
        actual_height, actual_width, actual_layers = actual.read()[1].shape
        self.assertEqual(expected_height, actual_height)
        self.assertEqual(expected_width, actual_width)
        self.assertEqual(expected_layers, actual_layers)

    def test_reverse_mp4_file(self):
        TestGifReverser.reverser.reverse_gif(
            TEST_MP4_NO_SOUND, OUTPUT_FILENAME)
        expected = cv2.VideoCapture(EXPECTED_MP4_NO_SOUND_REVERSED)
        actual = cv2.VideoCapture(OUTPUT_FILENAME)
        self.assertEqual(expected.get(cv2.CAP_PROP_FPS),
                         actual.get(cv2.CAP_PROP_FPS))
        expected_height, expected_width, expected_layers = expected.read()[
            1].shape
        actual_height, actual_width, actual_layers = actual.read()[1].shape
        self.assertEqual(expected_height, actual_height)
        self.assertEqual(expected_width, actual_width)
        self.assertEqual(expected_layers, actual_layers)
