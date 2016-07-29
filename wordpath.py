#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Justin Fay"
__author_email__ = "mail@justinfay.me"

"""
Excercise for workday interview.

Finding all wordpaths between two words.
Minor optimizations performed such as not using
recursion but still quite slow for large graphs.
"""

import sys

from collections import defaultdict
from itertools import izip_longest
from Queue import Queue


def read_words(path, length):
    """
    Return a set of all lines in a file at a given
    `path` whose length (excluding whitespace) is equal
    to `length`.
    """
    with open(path) as fh:
        return set(
            line.strip()
            for line in fh
            if len(line.strip()) == length)


def is_next_word(word1, word2):
    """
    Return `True` if the levenschtein distance between
    two words is exactly 1 otherwise `False`,
    """
    count = 0
    for a, b in izip_longest(word1, word2):
        # `bool` is a subclass of `int`.
        count += a != b
        if count > 1:
            return False
    return count == 1


def gen_next_words(start, words):
    """
    Return all the elements of `words` for which
    `is_next_word` returns `True` with first argument
    `start`.
    """
    for word in words:
        if is_next_word(start, word):
            yield word


def make_graph(start, words):
    """
    Construct a graph (adjacency list) with a given
    vertice `start` and possible vertices `words`.
    An edge is created between vertices where the
    levenschtein distance of words is exactly 1.
    """
    queue = Queue()
    queue.put(start)
    graph = defaultdict(set)
    while not queue.empty():
        next_ = queue.get()
        for word in gen_next_words(next_, words):
            graph[next_].add(word)
            if word not in graph:
                queue.put(word)
    return dict(graph)


def gen_word_paths(graph, start, end):
    """
    Generator method for finding all paths
    (using breath first search) between two
    points in a graph.
    """
    path = []
    queue = Queue()
    queue.put((start, end, path))
    while not queue.empty():
        start, end, path = queue.get()
        path = path + [start]
        if start == end:
            yield path
        for word in graph[start].difference(path):
            queue.put((word, end, path))


def are_valid_words(word1, word2, words):
    """
    Return `True` if `word1` and `word2` are of
    equal length and both are contained within `words`.
    """
    return (
        len(word1) == len(word2) and
        word1 in words and
        word2 in words)


def main(args):
    """
    The main entry point for wordpath.py

    Performs some sanitation checks on the args and
    calls the graph creation and path finding routines.
    """

    # Validation functionality.
    error = None
    try:
        word_path, start, end = args
        try:
            words = read_words(word_path, len(start))
            if not are_valid_words(start, end, words):
                error = ('Not valid input words, ensure words are '
                    'the same length and contained in the dictionary')
        except IOError:
            error = 'Cannot read word file.'
    except ValueError:
        error = ('Invalid arguments, usage: '
            'wordpath.py /path/to/words word1 word 2')

    if error is not None:
        sys.stderr.write(error + '\n')
        sys.exit(1)

    # Program execution.
    print "Constructing graph of all connected words."
    graph = make_graph(start, words)

    print "Attempting to find all word paths."
    paths_found = False
    for path in gen_word_paths(graph, start, end):
        paths_found = True
        print ' -> '.join(path)
    if not paths_found:
        print 'No valid word paths found.'


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
