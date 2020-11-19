import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from audiobook.helpers import Audiobook


class HelpersTestSuite(unittest.TestCase):
    """Testing the helper objects."""

    def test_audiobook_class(self):
        """Testing that the Audiobook class can load a template audiobook"""
        audiobook1_absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "~/tests/fixture/audiobook1.m4a"))
        audiobook1 = Audiobook(audiobook1_absolute_path)
        assert audiobook1.audiobook_file == audiobook1_absolute_path


if __name__ == "__main__":
    unittest.main()
