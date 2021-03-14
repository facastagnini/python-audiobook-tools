import logging
import pandas
import ssl
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from mutagen.easymp4 import EasyMP4


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
    self._original_metadata = Hash containing all the available
                              metadata that was read from the
                              audiobook file.

    """

    def __init__(self, audiobook_file):
        if audiobook_file is not None:
            self.audiobook_file = str(audiobook_file)
        self._original_metadata = self._read_metadata()

        # start with a copy of the original metadata
        self._updated_metadata = self._original_metadata

    def __repr__(self):
        return "This object abstracts the audiobook: %s" + self.audiobook_file

    def _read_metadata(self):
        """This method reads the metadata from the audiobook file."""

        metadata = EasyMP4(self.audiobook_file)
        return metadata

    def pprint(self):
        """return info about the current file, human friendly """

        # initialize the dictionaries
        info = {}
        metadata = {}

        # fill the dictionary with the data we want to print
        info["file"] = self.audiobook_file
        info["format"] = self._original_metadata.info.pprint()
        metadata["original"] = self._original_metadata.tags
        metadata["updated"] = self._updated_metadata.tags

        print(metadata)
        #logger.info(data)

        # finally, print the information
        print("File: {}".format(info["file"]))
        print("Format: {}\n".format(info["format"]))

        #header_horizontal = list(metadata['original'].keys() + metadata['original'].keys())
        #header_vertical = []

        return pandas.DataFrame(metadata)

        # ❯ python -m audiobook_tools info -f tests/fixtures/audible.m4b
        #
        # {'original': {'title': ['The Man Who Knew the Way to the Moon'], 'album': ['The Man Who Knew the Way to the Moon'], 'artist': ['Todd Zwillich'], 'albumartist': ['Todd Zwillich'], 'date': ['2019'], 'comment': ['Chapter 10'], 'genre': ['Audiobook'], 'copyright': ['©2019 Audible Originals, LLC (P)2019 Audible Originals, LLC.']}, 'updated': {'title': ['The Man Who Knew the Way to the Moon'], 'album': ['The Man Who Knew the Way to the Moon'], 'artist': ['Todd Zwillich'], 'albumartist': ['Todd Zwillich'], 'date': ['2019'], 'comment': ['Chapter 10'], 'genre': ['Audiobook'], 'copyright': ['©2019 Audible Originals, LLC (P)2019 Audible Originals, LLC.']}}
        # File: tests/fixtures/audible.m4b
        # Format: MPEG-4 audio (AAC LC), 1.02 seconds, 125589 bps
        #
        #       original      updated
        # 0        title        title
        # 1        album        album
        # 2       artist       artist
        # 3  albumartist  albumartist
        # 4         date         date
        # 5      comment      comment
        # 6        genre        genre
        # 7    copyright    copyright


        #####################################
        # python                                                                                                  writing-metadata ✱
        # Python 3.9.2 (default, Feb 24 2021, 10:08:03)
        # [Clang 10.0.0 (clang-1000.10.44.4)] on darwin
        # Type "help", "copyright", "credits" or "license" for more information.
        # >>> import pandas
        # >>> metadata = {'original': {'title': ['The Man Who Knew the Way to the Moon'], 'album': ['The Man Who Knew the Way to the Moon'], 'artist': ['Todd Zwillich'], 'albumartist': ['Todd Zwillich'], 'date': ['2019'], 'comment': ['Chapter 10'], 'genre': ['Audiobook'], 'copyright': ['©2019 Audible Originals, LLC (P)2019 Audible Originals, LLC.']}, 'updated': {'title': ['The Man Who Knew the Way to the Moon'], 'album': ['The Man Who Knew the Way to the Moon'], 'artist': ['Todd Zwillich'], 'albumartist': ['Todd Zwillich'], 'date': ['2019'], 'comment': ['Chapter 10'], 'genre': ['Cadorna'], 'copyright': ['©2019 Audible Originals, LLC (P)2019 Audible Originals, LLC.'], 'cover': ['diegote']}}
        #
        # >>> pandas.DataFrame(metadata)
        #                                                       original                                            updated
        # title                   [The Man Who Knew the Way to the Moon]             [The Man Who Knew the Way to the Moon]
        # album                   [The Man Who Knew the Way to the Moon]             [The Man Who Knew the Way to the Moon]
        # artist                                         [Todd Zwillich]                                    [Todd Zwillich]
        # albumartist                                    [Todd Zwillich]                                    [Todd Zwillich]
        # date                                                    [2019]                                             [2019]
        # comment                                           [Chapter 10]                                       [Chapter 10]
        # genre                                              [Audiobook]                                        [Audiobook]
        # copyright    [©2019 Audible Originals, LLC (P)2019 Audible ...  [©2019 Audible Originals, LLC (P)2019 Audible ...
        # chacho                                                     NaN                                   [this is a test]


class AudibleMetadata:
    """This class retrieves metadata from audible.com for a known asin number"""

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
        self.asin = self.validateasin(asin)
        self.url = self.buildurl()
        self.htmldata = self.fetchresource(self.url)
        self.extract()

    def validateasin(self, asin):
        """Clean and filter malformed asin"""
        asin = asin.strip()
        if len(asin) == 10 and asin.isalnum():
            return asin
        else:
            raise ValueError("asin has wrong lenght or invalid characters")

    def buildurl(self):
        """Build the url for the book page"""
        return URL_BASE + self.asin + TRAILING_OPTIONS

    def fetchresource(self, url):
        """Fetch the passed url, catch network errors if any"""

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            connection = urllib.request.urlopen(url, context=ctx)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            print("HTTPError: {}".format(e.code))
            raise ConnectionError
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print("URLError: {}".format(e.reason))
            raise ConnectionRefusedError
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
        self.tags["cover"] = self.fetchresource(self.tags["coverurl"])
