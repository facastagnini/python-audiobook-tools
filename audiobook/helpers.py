def get_answer():
    """Get an answer."""
    return True

# crear clase audiobook
# crear metodos
# actualizar tests

class Audiobook():
    """ This class helps abtract everything known about our audiobook.
    
    Attributes:
    self.audiobook_file = Audiobook file path (required)
    self._audiobook_file_current_metadata = Hash containing all the available metadata that was read from the audiobook file.

    """

    def __init__(self, audiobook_file):
        if audiobook_file != None:
            self.audiobook_file = str(audiobook_file)
        # self.team_losses = self._set_team_attr("losses")

        # initialize attributes with sane defaults
        #self.team_members = []
        #self.team_experience = 0.0

    def __repr__(self):
        return "This object abstracts the audiobook: %s" + self.audiobook_file