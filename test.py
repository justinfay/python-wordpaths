import wordpath


def test_is_next_word():
    assert wordpath.is_next_word('foo', 'boo')
    assert wordpath.is_next_word('2', '1')
    assert False == wordpath.is_next_word('f11', 'boo')


def test_gen_next_words():
    words = ['goo', 'foo', 'bang', 'bann']
    assert ['goo', 'foo'] == list(wordpath.gen_next_words('loo', words))
    assert [] == list(wordpath.gen_next_words('foooooo', words))
    assert ['bang', 'bann'] == list(wordpath.gen_next_words('banz', words))


def test_make_graph():
    words = ['cat', 'cag', 'cog', 'dog']
    expected = {
        'cat': set(['cag']),
        'cag': set(['cat', 'cog']),
        'cog': set(['cag', 'dog']),
        'dog': set(['cog']),
    }
    assert expected == wordpath.make_graph('cat', words)


def test_gen_word_paths():
    graph = {
        'cat': set(['cag']),
        'cag': set(['cat', 'cog']),
        'cog': set(['cag', 'dog']),
        'dog': set(['cog']),
    }
    expected = [['cat', 'cag', 'cog', 'dog']]
    assert expected == list(wordpath.gen_word_paths(graph, 'cat', 'dog'))


def test_are_valid_words():
    # Test with short circuit logic.
    assert False == wordpath.are_valid_words('goo', 'bar', [])

    assert False == wordpath.are_valid_words('goo', 'foo', ['foo'])
    assert wordpath.are_valid_words('goo', 'foo', ['goo', 'foo'])
