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


## Authors (in alphabetical order)
- @Diegus83
- @facastagnini
