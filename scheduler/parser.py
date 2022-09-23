"""Defines the command line parser for this package."""

from argparse import ArgumentParser

parser = ArgumentParser(
    description="Add the counters package to the Windows Task Scheduler"
)
parser.add_argument("path")
