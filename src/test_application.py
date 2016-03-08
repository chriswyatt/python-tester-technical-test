#!/usr/bin/env python

import unittest

from application import fizz_or_buzz


class TestFizzBuzz(unittest.TestCase):

    def test_returns_fizzbuzz(self):
        '''
        The fizz_or_buzz() method shall return 'fizzbuzz' if the number is
        evenly divisible by both 3 and 5
        '''
        result = fizz_or_buzz(15)
        self.assertEqual('fizzbuzz', result)


if __name__ == '__main__':
    unittest.main()
