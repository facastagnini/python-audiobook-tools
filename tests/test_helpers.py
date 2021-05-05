import os

import pytest

from audiobook_tools.helpers import AudibleMetadata, Audiobook


AUDIOBOOK_AUDIBLE = "fixtures/audible.m4b"
AUDIOBOOK_OVERDRIVE = "fixtures/overdrive.m4b"
AUDIOBOOK_INCOMPLETE_METADATA = "fixtures/author - title.m4b"


def audiobook_absolute_path(audiobook_file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), audiobook_file))


def get_audiobook(audiobook_file):
    """Testing that the Audiobook class can load an audiobook example"""
    return Audiobook(audiobook_absolute_path(audiobook_file))


def test_read_audible_audiobook():
    """Testing that the Audiobook class can load an audible template audiobook"""
    audiobook = get_audiobook(AUDIOBOOK_AUDIBLE)
    assert audiobook.audiobook_file == audiobook_absolute_path(AUDIOBOOK_AUDIBLE)


def test_read_overdrive_audiobook():
    """Testing that the Audiobook class can load an overdrive audiobook"""
    audiobook = get_audiobook(AUDIOBOOK_OVERDRIVE)
    assert audiobook.audiobook_file == audiobook_absolute_path(AUDIOBOOK_OVERDRIVE)


def test_read_audiobook_with_incomplete_metadata():
    """Testing that the Audiobook class can load an audiobook with incomplete metadata

    When an audiobook is missing metadata required to identify it,
    we resort to the filename.

    This audiobook is missing all the metadata that could help identify it,
    test with the filename based id mechanism.
    """
    audiobook = get_audiobook(AUDIOBOOK_INCOMPLETE_METADATA)
    assert audiobook.audiobook_file == audiobook_absolute_path(AUDIOBOOK_INCOMPLETE_METADATA)


def test_pprint_audible_audiobook():
    """Testing that the Audiobook class can load an audible template audiobook"""
    audiobook = get_audiobook(AUDIOBOOK_AUDIBLE)

    pprint_output = """Format: MPEG-4 audio (AAC LC), 1.02 seconds, 125589 bps

                                                  Original metadata                                        Updated metadata
title                        [The Man Who Knew the Way to the Moon]                  [The Man Who Knew the Way to the Moon]
album                        [The Man Who Knew the Way to the Moon]                  [The Man Who Knew the Way to the Moon]
artist                                              [Todd Zwillich]                                         [Todd Zwillich]
albumartist                                         [Todd Zwillich]                                         [Todd Zwillich]
date                                                         [2019]                                                  [2019]
comment                                                [Chapter 10]                                            [Chapter 10]
genre                                                   [Audiobook]                                             [Audiobook]
copyright    [©2019 Audible Originals, LLC (P)2019 Audible Origi...  [©2019 Audible Originals, LLC (P)2019 Audible Origi..."""

    assert audiobook.pprint() == pprint_output


def test_pprint_overdrive_audiobook():
    """Testing that the Audiobook class can load an audible template audiobook"""
    audiobook = get_audiobook(AUDIOBOOK_OVERDRIVE)

    pprint_output = """Format: MPEG-4 audio (AAC LC), 1.04 seconds, 69847 bps

                                                  Original metadata                                        Updated metadata
title                                        [Talking to Strangers]                                  [Talking to Strangers]
album        [Talking to Strangers - What We Should Know about t...  [Talking to Strangers - What We Should Know about t...
artist                                           [Malcolm Gladwell]                                      [Malcolm Gladwell]
albumartist                                      [Malcolm Gladwell]                                      [Malcolm Gladwell]
comment      [<p></p><p>Malcolm Gladwell, host of the podcast Re...  [<p></p><p>Malcolm Gladwell, host of the podcast Re...
description  [<p></p><p>Malcolm Gladwell, host of the podcast Re...  [<p></p><p>Malcolm Gladwell, host of the podcast Re...
genre                             [Nonfiction/Psychology/Sociology]                       [Nonfiction/Psychology/Sociology]
copyright                                     [Hachette Book Group]                                   [Hachette Book Group]"""

    assert audiobook.pprint() == pprint_output


def test_pprint_audiobook_with_incomplete_metadata():
    """Testing that the Audiobook class can load an audible template audiobook"""
    audiobook = get_audiobook(AUDIOBOOK_INCOMPLETE_METADATA)

    pprint_output = """Format: MPEG-4 audio (AAC LC), 1.02 seconds, 125590 bps

Empty DataFrame
Columns: [Original metadata, Updated metadata]
Index: []"""

    assert audiobook.pprint() == pprint_output


@pytest.fixture(scope="session")  # one audiobook to rule'em all
def b():
    """Create an AudibleMetadata object to be used by all subsequent tests"""
    b = AudibleMetadata("B002UZJGYY")
    return b


def test_asin_validation(b):
    """Testing that we can clean and validate the asin"""
    assert b.validateasin(" B002UZJGYY ") == "B002UZJGYY"


def test_metadata_extraction(b):
    """Testing that we can extract the info we are interested in"""
    assert b.tags["author"] == ["Arthur C. Clarke"]
