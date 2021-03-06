#!/usr/bin/env python3

# Chris Wyatt - 1:45am

# Python 2, 3 support
from __future__ import print_function
from six.moves import input

import sys

import requests
from bs4 import BeautifulSoup


def get(a):
    '''
    Performs a HTTP request, returning the response text
    '''
    response = requests.get(a)
    return response.text


def element_count(a, b):
    '''
    Element count
    '''
    output = get(a)

    soup = BeautifulSoup(output, 'html.parser')

    return len(soup.find_all(b))


def fizz_or_buzz(number):
    '''
    Return divisors of a number (but only check if 3 and 5) 
    '''
    is_three = True if number % 3 == 0 else False
    is_five = True if number % 5 == 0 else False

    if is_three and is_five:
        return [3, 5]
    elif is_three:
        return [3]
    elif is_five:
        return [5]
    else:
        return []


def app_output(url, tag, count, divisors):
    '''
    Output to stdout and file
    '''
    line = "URL: '{}', tag: '{}', count: {}, divisors: [{}]".format(
        url, tag, count, ', '.join(str(d) for d in divisors))
    with open('output.txt', 'a') as fd:
        fd.write(line + '\n')
    print(line)


def app(url, tag):
    count = element_count(url, tag)
    divisors = fizz_or_buzz(count)
    app_output(url, tag, count, divisors)


if __name__ == '__main__':
    # Application will take two args: URL, HTML tag type (a, ul, div, ...etc)
    if len(sys.argv) == 1:
        url = input('URL: ')
        tag = input('Tag: ')
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        tag = sys.argv[2]
    else:
        sys.stderr.write('Command takes 2 arguments: URL and tag\n')
        sys.exit(1)

    app(url, tag)


'''
Review comments:

PEP8:
application.py:13:1: E302 expected 2 blank lines, found 1
application.py:18:1: E302 expected 2 blank lines, found 1
application.py:26:1: E302 expected 2 blank lines, found 1
application.py:44:1: E302 expected 2 blank lines, found 1
application.py:49:1: E302 expected 2 blank lines, found 1
application.py:49:10: E231 missing whitespace after ','
application.py:50:28: E231 missing whitespace after ','
application.py:52:17: E231 missing whitespace after ','
application.py:52:19: E231 missing whitespace after ','
application.py:52:25: E231 missing whitespace after ','
application.py:54:1: E402 module level import not at top of file
application.py:56:80: E501 line too long (80 > 79 characters)

Comment at top looks a bit like Python 2.3. A space after the comma will make it
less misleading.

In if __name__ == '__main__' block, it would be good to raise an error if
len(sys.argv) does not equal 1 or 3

Line 49: a, b are not helpful names. May as well be url, tag.

Line 44: No reason for variable length of args

Line 46 and 47: String is repeated. Consider creating a variable.

Line 46 and 47: Output is not descriptive and using = as separator is confusing
and unusual. Something like: "URL: 'http://foo', tag: 'bar', evenly divisible by
3 and 5" would be more descriptive.

Line 14, 19, 27: Better to use multiline comments for functions/method
documentation

Line 44: No docstring.

Line 28: Comment does not make it clear that number divides without remainders.
It would be better to describe than use math symbols.
fizz_or_buzz(): Function could be more generic and not use cryptic words 'fizz'
and 'buzz'. You could pass in list of factorials and return dictionary of which
ones divide without remainders (with factorials as keys, and a boolean
mentioning whether there are remainders). You could delegate string formatting
to another function.

Line 32: I think '' would be clearer than <empty>. Docstring generally could
make it clearer that strings are being returned, e.g. 'fizz', 'buzz' etc.
Consider allowing multiple tags to be passed in, so tags could be processed in
batch

Consider adding shebang line at the top

Probably could make all methods except app() private

app() could be renamed to something more desriptive, in case anyone wants to
import it into another module.

Name of module is also undescriptive (application.py)

Line 54: Import should be at the top

Line 7: import not used

Line 9: import not used

Warning displayed when running application: 'UserWarning: No parser was
explicitly specified, so I'm using the best available HTML parser for this
system ("html.parser"). This usually isn't a problem, but if you run this code
on another system, or in a different virtual environment, it may use a
different parser and behave differently.'
'''
