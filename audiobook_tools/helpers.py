import logging
from mutagen.mp4 import MP4  # , MP4Cover

logger = logging.getLogger(__name__)


def get_answer():
    """Get an answer."""
    return True


class Audiobook:
    """This class helps abtract everything known about an audiobook.

    Attributes:
    self.audiobook_file = Audiobook file path (required)
    self._audiobook_file_current_metadata = Hash containing all the available
                                            metadata that was read from the
                                            audiobook file.

    """

    def __init__(self, audiobook_file):
        if audiobook_file is not None:
            self.audiobook_file = str(audiobook_file)
        self.original_metadata = self._read_metadata()
        # print(self.original_metadata())

    def __repr__(self):
        return "This object abstracts the audiobook: %s" + self.audiobook_file

    def _read_metadata(self):
        """This method reads the metadata from the audiobook file.

        # manual run...
        # ❯ python3
        # Python 3.9.0 (default, Oct 27 2020, 14:23:31)
        # [Clang 10.0.0 (clang-1000.11.45.5)] on darwin
        # >>> from mutagen.mp4 import MP4
        # >>> MP4("TsaryEdition_ep6.m4a")
        # {
        # '©nam': ['The Phoenix Project: A Novel about IT, DevOps, ...'],
        # '©ART': ['Gene Kim, Kevin Behr, George Spafford'],
        # 'aART': ['Gene Kim, Kevin Behr, George Spafford'],
        # '©alb': ['The Phoenix Project: A Novel about IT, DevOps, ...'],
        # '©day': ['2015'],
        # '©too': ['Lavf58.45.100'],
        # '©cmt': ['Chapter 48'],
        # '©gen': ['Audiobook'],
        # 'cprt': ['©2014 Gene Kim, Kevin Behr, and George Spafford...'],
        # 'covr': [MP4Cover(b'\xff
        """

        # try:
        metadata = MP4(self.audiobook_file)
        return metadata
