import logging

from mutagen.easymp4 import EasyMP4


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
        self.metadata = self.original_metadata

    def __repr__(self):
        return "This object abstracts the audiobook: %s" + self.audiobook_file

    def _read_metadata(self):
        """This method reads the metadata from the audiobook file."""

        # try:
        metadata = EasyMP4(self.audiobook_file)
        return metadata

    def pprint(self):
        """return a lot of info about the current file"""

        ret = {}
        ret["file"] = self.audiobook_file
        ret["info"] = self.metadata.info.pprint()

        return ret
