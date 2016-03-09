#!/usr/bin/env python3

import unittest
import six

from requests.exceptions import ConnectionError
from mock import patch, Mock, MagicMock, mock_open, call, sentinel

from application import fizz_or_buzz, element_count, app_output, app


class TestElementCount(unittest.TestCase):

    def setUp(self):
        self.url = 'http://foo.com/'
        self.tag = 'br'
        self.response_text = 'Foo<br>Bar<br>Baz'
        self.parser = 'html.parser'

    @patch('application.BeautifulSoup')
    @patch('application.requests')
    def test_success(self, requests_mock, BeautifulSoupMock):
        '''
        element_count() shall use requests and bs4 to return the number of
        elements
        '''
        response_mock = Mock()
        response_mock.text = self.response_text
        requests_mock.get.return_value = response_mock

        find_all_return_value_mock = MagicMock()
        find_all_return_value_mock.__len__.return_value = 123

        beautiful_soup_mock = Mock()
        beautiful_soup_mock.find_all.return_value = find_all_return_value_mock

        BeautifulSoupMock.return_value = beautiful_soup_mock

        result = element_count(self.url, self.tag)
        self.assertEqual(123, result)

        requests_mock.get.assert_called_once_with(self.url)
        BeautifulSoupMock.assert_called_once_with(
            self.response_text, self.parser)
        beautiful_soup_mock.find_all.assert_called_once_with(self.tag)

    @patch('application.BeautifulSoup')
    @patch('application.requests')
    def test_raises_connection_error(self, requests_mock, BeautifulSoupMock):
        '''
        element_count() shall raise a ConnectionError if requests.get() raises
        a ConnectionError
        '''
        requests_mock.get.side_effect = ConnectionError

        self.assertRaises(ConnectionError, element_count, self.url, self.tag)

        requests_mock.get.assert_called_once_with(self.url)
        BeautifulSoupMock.assert_not_called()


class TestFizzOrBuzz(unittest.TestCase):

    def test_number_divisible_by_3_and_5(self):
        '''
        The fizz_or_buzz() method shall return 'fizzbuzz' if the number is
        evenly divisible by both 3 and 5
        '''
        result = fizz_or_buzz(15)
        six.assertCountEqual(self, [3, 5], result)

    def test_number_divisible_by_3_not_5(self):
        '''
        The fizz_or_buzz() method shall return 'fizz' if the number is evenly
        divisible by 3 and not 5
        '''
        result = fizz_or_buzz(6)
        six.assertCountEqual(self, [3], result)

    def test_number_divisible_by_5_not_3(self):
        '''
        The fizz_or_buzz() method shall return 'buzz' if the number is evenly
        divisible by 5 and not 3
        '''
        result = fizz_or_buzz(10)
        six.assertCountEqual(self, [5], result)

    def test_number_equals_3(self):
        '''
        The fizz_or_buzz() method shall return 'fizz' if the number is equal to
        3
        '''
        result = fizz_or_buzz(3)
        six.assertCountEqual(self, [3], result)

    def test_number_equals_5(self):
        '''
        The fizz_or_buzz() method shall return 'buzz' if the number is equal to
        5
        '''
        result = fizz_or_buzz(5)
        six.assertCountEqual(self, [5], result)

    def test_number_not_divisible_by_3_or_5(self):
        '''
        The fizz_or_buzz() method shall return '' if the number is not evenly
        divisible by 3 or 5
        '''
        result = fizz_or_buzz(4)
        six.assertCountEqual(self, [], result)

    def test_number_equals_0(self):
        '''
        The fizz_or_buzz() method shall return 'fizzbuzz' if the number is
        equal to 0
        '''
        result = fizz_or_buzz(0)
        six.assertCountEqual(self, [3, 5], result)

    def test_string_raises_exception(self):
        '''
        A TypeError shall be raised if fizzbuzz() is called with its 'number'
        argument set to a string
        '''
        self.assertRaises(TypeError, fizz_or_buzz, 'foo')


class TestAppOutput(unittest.TestCase):

    def setUp(self):
        self.url = 'http://foo.com/'
        self.tag = 'br'
        self.count = 123
        self.divisors = [1, 2, 3]

    @patch('application.print')
    def test_success(self, print_mock):
        '''
        app_output() shall write to output.txt and print the output using the
        print() function
        '''
        open_mock = mock_open()
        with patch('application.open', open_mock):
            app_output(self.url, self.tag, self.count, self.divisors)
        open_mock.assert_called_once_with('output.txt', 'a')
        handle_mock = open_mock()
        handle_mock.write.assert_called_once_with(
            "URL: '{}', tag: '{}', count: {}, divisors: [{}]\n".format(
                self.url, self.tag, self.count,
                ', '.join(str(d) for d in self.divisors)))

        print_mock.assert_called_once_with(
            "URL: '{}', tag: '{}', count: {}, divisors: [{}]".format(
                self.url, self.tag, self.count, 
                ', '.join(str(d) for d in self.divisors)))

    @patch('application.print')
    def test_raises_io_error(self, print_mock):
        '''
        app_output() shall raise an IOError if the file handle raises an
        IOError
        '''
        handle_mock = MagicMock()
        handle_mock.__enter__.side_effect = IOError

        open_mock = mock_open()
        open_mock.return_value = handle_mock

        with patch('application.open', open_mock):
            self.assertRaises(IOError, app_output, self.url, self.tag,
                              self.count, self.divisors)
        open_mock.assert_called_once_with('output.txt', 'a')

        print_mock.assert_not_called()


class TestApp(unittest.TestCase):

    @patch('application.app_output')
    @patch('application.fizz_or_buzz')
    @patch('application.element_count')
    def test_success(self, element_count_mock, fizz_or_buzz_mock,
                     app_output_mock):
        '''
        app() shall call the appropriate functions and pass the correct
        arguments
        '''
        element_count_mock.return_value = sentinel.count
        fizz_or_buzz_mock.return_value = sentinel.divisors

        app(sentinel.url, sentinel.tag)
        element_count_mock.assert_called_once_with(sentinel.url, sentinel.tag)
        fizz_or_buzz_mock.assert_called_once_with(sentinel.count)
        app_output_mock.assert_called_once_with(
            sentinel.url,
            sentinel.tag,
            sentinel.count,
            sentinel.divisors)


if __name__ == '__main__':
    unittest.main()
