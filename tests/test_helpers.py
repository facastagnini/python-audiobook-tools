import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from audiobook_tools.helpers import Audiobook

AUDIOBOOK_AUDIBLE = "fixtures/audible.m4b"
AUDIOBOOK_OVERDRIVE = "fixtures/overdrive.m4b"
AUDIOBOOK_INCOMPLETE_METADATA = "fixtures/author - title.m4b"


class AudiobookClassTestSuite(unittest.TestCase):
    """Testing the helper objects."""

    def read_audiobook(self, audiobook_file):
        """Testing that the Audiobook class can load an audiobook example"""
        audiobook_absolute_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), audiobook_file))
        audiobook = Audiobook(audiobook_absolute_path)
        assert audiobook.audiobook_file == audiobook_absolute_path

    def test_read_audible_audiobook(self):
        """Testing that the Audiobook class can load an audible template audiobook"""
        self.read_audiobook(AUDIOBOOK_AUDIBLE)

    def test_read_overdrive_audiobook(self):
        """Testing that the Audiobook class can load an overdrive audiobook"""
        self.read_audiobook(AUDIOBOOK_AUDIBLE)

    def test_read_audiobook_with_incomplete_metadata(self):
        """Testing that the Audiobook class can load an audiobook with incomplete metadata

        When an audiobook is missing metadata required to identify it,
        we resort to the filename.

        This audiobook is missing all the metadata that could help identify it,
        therefor testing the filename based id mechanism.
        """
        self.read_audiobook(AUDIOBOOK_INCOMPLETE_METADATA)


if __name__ == "__main__":
    unittest.main()
