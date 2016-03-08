#!/usr/bin/env python

import unittest

from application import fizz_or_buzz


class TestFizzBuzz(unittest.TestCase):

    def test_number_divisible_by_3_and_5(self):
        '''
        The fizz_or_buzz() method shall return 'fizzbuzz' if the number is
        evenly divisible by both 3 and 5
        '''
        result = fizz_or_buzz(15)
        self.assertEqual('fizzbuzz', result)

    def test_number_divisible_by_3_not_5(self):
        '''
        The fizz_or_buzz() method shall return 'fizz' if the number is evenly
        divisible by 3 and not 5
        '''
        result = fizz_or_buzz(6)
        self.assertEqual('fizz', result)

    def test_number_divisible_by_5_not_3(self):
        '''
        The fizz_or_buzz() method shall return 'buzz' if the number is evenly
        divisible by 5 and not 3
        '''
        result = fizz_or_buzz(10)
        self.assertEqual('buzz', result)

    def test_number_equals_3(self):
        '''
        The fizz_or_buzz() method shall return 'fizz' if the number is equal to
        3
        '''
        result = fizz_or_buzz(3)
        self.assertEqual('fizz', result)

    def test_number_equals_5(self):
        '''
        The fizz_or_buzz() method shall return 'buzz' if the number is equal to
        5
        '''
        result = fizz_or_buzz(5)
        self.assertEqual('buzz', result)

    def test_number_not_divisible_by_3_or_5(self):
        '''
        The fizz_or_buzz() method shall return '' if the number is not evenly
        divisible by 3 or 5
        '''
        result = fizz_or_buzz(4)
        self.assertEqual('', result)

    def test_number_equals_0(self):
        '''
        The fizz_or_buzz() method shall return 'fizzbuzz' if the number is equal
        to 0
        '''
        result = fizz_or_buzz(0)
        self.assertEqual('fizzbuzz', result)

    def test_string_raises_exception(self):
        '''
        A TypeError shall be raised if fizzbuzz() is called with its 'number'
        argument set to a string
        '''
        self.assertRaises(TypeError, fizz_or_buzz, 'foo')
        


if __name__ == '__main__':
    unittest.main()
