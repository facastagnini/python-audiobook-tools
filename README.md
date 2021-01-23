![Python package](https://github.com/facastagnini/python-audiobook-tools/workflows/Python%20package/badge.svg)

# python-audiobook-tools

This project aims to create a few tools used to standarize audiobooks for Plex.
Mostly a project suited to fit the needs of the authors.

## Installation
### Install from pypi (pending, not yet published)
### Install from source
```
$ git clone git@github.com:facastagnini/python-audiobook-tools.git
$ cd python-audiobook-tools
$ pip3 install .
$ audiobook_tools -v
usage: audiobook_tools [-h] [-v] [-t TIMEOUT] {info} ...

A swiss army knife for audiobook metadata enrich.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable more verbose messages for debugging
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout (seconds) for network requests. Default 10.

Available commands:
  {info}                To get more help, use the -h option with the command.
    info                Get information about an audiobook file

Version 0.1.0. [Python 3.9.1-darwin] Source at https://github.com/facastagnini/python-audiobook-tools/
```

## Usage (WIP)

```
$ audiobook_tools info -h 
```

## Development

```
git clone git@github.com:facastagnini/python-audiobook-tools.git
cd python-audiobook-tools

pip install .

make test # to make sure everything works before making changes

# go ahead and make your changes...

make test # to make sure you didnt break things

# open a PR
```

### ROADMAP

The tool should:
- [ ] take an audiobook file as a parameter
- [ ] verify the format is correct (M4B)
- [ ] search audible for the first x matches (default to 5)
- [ ] present a table with the matches, the user picks one as the correct one
- [ ] fetch metadata for the selected result
- [ ] prenset a diff table showing all the fields and a before and after. example

tag/field | original value | new value
--------- | -------------- | ---------
author | H.P.Lovecraft | Howard Phillips Lovecraft
name | At the mountains of... | At the Mountains of Madness
published | 1997 | 12-01-1997

- [ ] apply the update? [y/n]
- [ ] write the change


## Authors (in alphabetical order)
- @Diegus83
- @facastagnini
