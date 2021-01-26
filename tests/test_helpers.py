import os

from audiobook_tools.helpers import Audiobook


AUDIOBOOK_AUDIBLE = "fixtures/audible.m4b"
AUDIOBOOK_OVERDRIVE = "fixtures/overdrive.m4b"
AUDIOBOOK_INCOMPLETE_METADATA = "fixtures/author - title.m4b"


def read_audiobook(audiobook_file):
    """Testing that the Audiobook class can load an audiobook example"""
    audiobook_absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), audiobook_file))
    audiobook = Audiobook(audiobook_absolute_path)
    assert audiobook.audiobook_file == audiobook_absolute_path


def test_read_audible_audiobook():
    """Testing that the Audiobook class can load an audible template audiobook"""
    read_audiobook(AUDIOBOOK_AUDIBLE)


def test_read_overdrive_audiobook():
    """Testing that the Audiobook class can load an overdrive audiobook"""
    read_audiobook(AUDIOBOOK_AUDIBLE)


def test_read_audiobook_with_incomplete_metadata():
    """Testing that the Audiobook class can load an audiobook with incomplete metadata

    When an audiobook is missing metadata required to identify it,
    we resort to the filename.

    This audiobook is missing all the metadata that could help identify it,
    test with the filename based id mechanism.
    """
    read_audiobook(AUDIOBOOK_INCOMPLETE_METADATA)
