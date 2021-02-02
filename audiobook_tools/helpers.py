import logging
import ssl
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from mutagen.mp4 import MP4  # , MP4Cover


logger = logging.getLogger(__name__)

URL_BASE = "https://www.audible.com/pd/"
TRAILING_OPTIONS = "?ipRedirectOverride=true"


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


class AudibleMetadata:
    """This class retrieves metadata from audible.com for a known asin number
    # This is the same test that's in the test file
    #>>> b = AudibleMetadata('B002UZJGYY')
    #>>> b.asinisvalid()
    #True
    """

    def __init__(self, asin):
        self.asin = ""
        self.htmldata = ""
        self.url = ""
        self.tags = {
            "audibleurl": "",
            "author": [],
            "title": "",
            "subtitle": "",
            # "release": '', # work in progress
            "narrator": [],
            "series": [],
            "duration": "",
            "categories": [],
            "summary": "",
            "copyright": "",
            "asin": "",
            "coverurl": "",
            "cover": "",
        }
        self.asin = asin.strip()
        if not self.asinisvalid():
            raise ValueError("asin estructure is not valid")
        self.fetchresource()
        self.extract()

    def asinisvalid(self):
        """Validates the asin structure"""
        if len(self.asin) == 10 and self.asin.isalnum():
            return True
        else:
            return False

    def fetchresource(self, coverurl=None):
        """Build the url, fetch the html, catch network errors if any
        Also fetch covert art if the proper argument is passed
        """

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.url = URL_BASE + self.asin + TRAILING_OPTIONS

        try:
            if coverurl is None:
                connection = urllib.request.urlopen(self.url, context=ctx)
            else:
                connection = urllib.request.urlopen(coverurl, context=ctx)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            print("HTTPError: {}".format(e.code))
            raise ConnectionError

        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print("URLError: {}".format(e.reason))
            raise ConnectionRefusedError
        else:
            if coverurl is None:
                self.htmldata = connection.read().decode("utf-8")
            else:
                return connection.read()

    def extract(self):
        """extract the metadata from the html object using bs4"""

        soup = BeautifulSoup(self.htmldata, "html.parser")

        # asin and audible url
        self.tags["audibleurl"] = self.url
        self.tags["asin"] = self.asin

        # author/s
        for i in soup.find("li", class_="authorLabel").find_all("a"):
            self.tags["author"].append(i.string)

        # title
        self.tags["title"] = soup.find("meta", property="og:title")["content"]

        # subtitle/s
        try:
            self.tags["subtitle"] = soup.find_all("li", class_="bc-spacing-s2")[0].find("span").string

        except IndexError:
            pass

        # narrator/s
        for i in soup.find("li", class_="narratorLabel").find_all("a"):
            self.tags["narrator"].append(i.string)

        # series name
        try:
            for i in soup.find("li", class_="seriesLabel").find_all("a"):
                self.tags["series"].append(i.string)

        except IndexError:
            pass

        # duration
        self.tags["duration"] = soup.find("li", class_="runtimeLabel").string.splitlines()[3].strip()

        # categories
        for i in soup.find("li", class_="categoriesLabel").find_all("a"):
            self.tags["categories"].append(i.string)

        # summary
        self.tags["summary"] = soup.find_all("span", class_="bc-text bc-color-secondary")[0].text

        # copyrigh
        self.tags["copyright"] = soup.find_all("span", class_="bc-text bc-color-secondary")[1].text

        # coverurl
        self.tags["coverurl"] = soup.find_all("img")[1]["src"]

        # cover art
        self.tags["cover"] = self.fetchresource(coverurl=self.tags["coverurl"])
