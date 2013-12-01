import unittest
from decorators import limitable
import itertools


@limitable
def gen1():
    for i in itertools.count():
        yield i


@limitable
def gen2(n):
    for i in xrange(n):
        yield i


class LimitableTests(unittest.TestCase):
    def test_gen1_limitable(self):
        n = 5
        limited = gen1(limit=n)
        actual = tuple(limited)
        expected = tuple(range(n))
        self.assertEquals(actual, expected)

    def test_gen2_minus_1(self):
        n = 5
        limited = gen2(n, limit=n - 1)
        actual = tuple(limited)
        expected = tuple(range(n - 1))
        self.assertEquals(actual, expected)

    def test_gen2_plus_1(self):
        n = 5
        limited = gen2(n, limit=n + 1)
        actual = tuple(limited)
        expected = tuple(range(n))
        self.assertEquals(actual, expected)
