import unittest
import cv2
from window_utils import find_agario


class TestInterface(unittest.TestCase):
    def test_find_agario(self):
        # requires the agario window to be open
        window = find_agario()
        self.assertIsNotNone(window)