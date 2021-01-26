import argparse
import sys
import urllib.error
import urllib.request as request

from bs4 import BeautifulSoup


urlbase = "https://www.audible.com/pd/"
trailingoptions = "?ipRedirectOverride=true"


def main(args):
    parser = argparse.ArgumentParser(prog="audible", description="Parse audiobook metadata from Audible.")
    parser.add_argument("-i", "--interactive", help="Interactive mode", action="store_true")
    parser.add_argument("-A", "--asin", help="Provide an asin number")
    parser.add_argument("-a", "--author", help="Search by author name")
    parser.add_argument("-t", "--title", help="Search by book title")

    opts = parser.parse_args(args)

    if opts.interactive:
        repl()
    if opts.asin:
        if validate_asin(opts.asin):
            scrape(opts.asin)
        else:
            print("Not a valid asin lenght")
            quit()
    if opts.author:
        findbook(opts.author)
    if opts.title:
        findbook(opts.title)


def repl():
    """
    In interactive mode the prompt will ask for an asin number,
    if valid it will fetch the metadata from audible and print to stdou
    """
    print("Enter asin # (10 alphanumeric characters)")
    print("Hit Ctrl-C to exit")
    while True:
        try:
            asin = input("asin #: ")
        except KeyboardInterrupt:
            print("Goodbye!")
            break
        if validate_asin(asin):
            scrape(asin)
        else:
            print("Not a valid asin lenght")


def validate_asin(asin):
    """
    Check for a properly formatted asin #
    This doesn't mean the asin exist in Audible, onlt that is properly formatted
    """
    if len(asin) == 10 and asin.isalnum():
        return True
    else:
        return False


def assembleurl(asin=None, author=None, title=None):
    """
    Assemble the audible URL.
    If an asin# is provided the URL will go directly to the book page.
    If author/title are provided the URL will perform a search in audible with those terms (not implemented yet)
    """
    if asin:
        url = urlbase + asin + trailingoptions
    elif author or title:
        print("Not implemented")
        quit()
    return url


def fetch_html(url):
    """
    Given a possible URL for the book page, fetch the HTML and save it as data object
    We can get a 404 error if the asin # doesn't exist
    """
    # try to catch http errors
    try:
        connection = request.urlopen(url)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print("HTTPError: {}".format(e.code))
        quit()
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print("URLError: {}".format(e.reason))
        quit()
    else:
        data = connection.read()
        return data


def scrape(asin=None):
    """
    We only scrape once we have an asin number, either provided by the
    user or found using the author/title search (not implemmented yet)
    """
    url = assembleurl(asin)
    data = fetch_html(url)
    # create soup element for parsing
    soup = BeautifulSoup(data, "html.parser")

    # create empty dictionary for the date we are goign to scrape
    tags = {
        "audibleURL": url,
        "author": [],
        "title": "",
        "subtitle": "",
        # 'release': '', # we can't access the full release date unless we are authenticated or from the results page
        "narrator": [],
        "series": [],
        "duration": "",  # this may be useful for disambiguation in the future
        "categories": [],
        "summary": "",
        "copyright": "",
        "asin": asin,
    }

    # begin parsing and extracting
    for i in soup.find("li", class_="authorLabel").find_all("a"):
        tags["author"].append(i.string)

    tags["title"] = soup.find("meta", property="og:title")["content"]

    try:
        tags["subtitle"] = soup.find_all("li", class_="bc-spacing-s2")[0].find("span").string

    except IndexError:
        tags["subtitle"] = ""

    for i in soup.find("li", class_="narratorLabel").find_all("a"):
        tags["narrator"].append(i.string)

    try:
        for i in soup.find("li", class_="seriesLabel").find_all("a"):
            tags["series"].append(i.string)

    except IndexError:
        tags["series"] = ""

    tags["duration"] = soup.find("li", class_="runtimeLabel").string.splitlines()[3].strip()

    for i in soup.find("li", class_="categoriesLabel").find_all("a"):
        tags["categories"].append(i.string)

    tags["summary"] = soup.find_all("span", class_="bc-text bc-color-secondary")[0].text

    tags["copyright"] = soup.find_all("span", class_="bc-text bc-color-secondary")[1].text

    present(tags)

    return tags


def present(tags):
    """
    We do an ordered print of the scraped tags. This can be reused when we have the
    capabilities to show multiple results
    """
    for key in tags:
        print(f"{key}= {tags[key]}")


def findbook(query):
    print("Not implemented")


if __name__ == "__main__":
    main(sys.argv[1:])
