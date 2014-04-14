"""
A python implementation of https://github.com/DaveChild/Text-Statistics/.
I saw it and really liked the idea.

All functions take a string and return a Decimal score.
"""

from decimal import Decimal as D
#Commented below because Counter is available first in python 2.7
#instead added ported version in this file at end.
#from collections import Counter
from math import sqrt
import re
import sys
import string
from Products.CMFCore.utils import getToolByName

def html_to_text(context, html):
    """given html returns plain text
    """
    transforms = getToolByName(context, 'portal_transforms')
    stream = transforms.convertTo('text/plain', html, mimetype='text/html')
    text = stream.getData().strip()

    return text

def normalise_text(text):
    """normalise text by removing/replacing certain characters
    """
    # Replace commas, hyphens etc (count them as spaces)
    textclean = text.translate(string.maketrans("[]{}()'/-:;,", "            "))

    # unify terminators
    textclean = textclean.replace('?','.')
    textclean = textclean.replace('!','.')

    # replace new lines with spaces
    textclean = textclean.replace('\r\n',' ')
    textclean = textclean.replace('\n',' ')
    textclean = textclean.replace('\r',' ')

    # remove multiple spaces
    textclean = textclean.replace('  ',' ')

    # removed double terminators
    textclean = textclean.replace('..','.')
    textclean = textclean.replace('. .','.')
    textclean = textclean.replace('.  .','.')

    return textclean

def flesch_kincaid_reading_ease(text):
    """https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
    """
    text = clean_text(text)

    words = _count_words(text)
    sentences = _count_sentences(text)
    syllables = _count_syllables(text)

    words_over_sentences = words / sentences
    syllables_over_words = syllables / words

    score = D('206.835') - (D('1.015') * words_over_sentences) - \
                    (D('84.6') * syllables_over_words)

    return score

def flesch_kincaid_grade_level(text):
    """https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    """
    text = clean_text(text)

    words = _count_words(text)
    sentences = _count_sentences(text)
    syllables = _count_syllables(text)

    words_over_sentences = words / sentences
    syllables_over_words = syllables / words

    score = (D('0.39') * words_over_sentences) + (D('11.8') * \
                    syllables_over_words) - D('15.59')

    return score

def gunning_fog_score(text):
    """https://en.wikipedia.org/wiki/Gunning_fog_index
    0.4 * ((words / sentences) + 100 * (complex_words / words))
    """
    text = clean_text(text)

    words = _count_words(text)
    sentences = _count_sentences(text)
    complex_words = _count_complex_words(text)

    words_over_sentences = words / sentences
    complex_over_normal = complex_words / words

    score = D('0.4') * (words_over_sentences + (100 * complex_over_normal))

    return score

def coleman_liau_index(text):
    """https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
    Lower = Easier to read

    L = average number of letters per 100 words
    S = average number of sentences per 100 words
    (0.0588 * L) - (0.296 * S) - 15.8
    """
    text = clean_text(text)

    words = _count_words(text)
    sentences = _count_sentences(text)
    letters = _count_letters(text)

    L = (letters / words) * D('100')
    S = (sentences / words) * D('100')

    score = (D('0.0588') * L) - (D('0.296') * S) - D('15.8')

    return score

def smog_index(text):
    """https://en.wikipedia.org/wiki/SMOG

    1.043 * sqrt(polysyllables * (30 / sentences) + 3.1291)
    """
    text = clean_text(text)

    sentences = _count_sentences(text)
    polysyllables = _count_complex_words(text)

    score = D('1.043') * D(sqrt(polysyllables * (D('30') / sentences) + \
                    D('3.1291')))

    return score

def automated_readability_index(text):
    """https://en.wikipedia.org/wiki/Automated_Readability_Index

    4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
    """
    text = clean_text(text)

    words = _count_words(text)
    sentences = _count_sentences(text)
    letters = _count_letters(text)

    score = D('4.71') * (letters / words) + (D('0.5') * \
                    (words / sentences)) - D('21.43')

    return score

def clean_text(text):
    """ Clean text
    """

    return text
    #static $clean = array();

    #if (isset($clean[$strText])) {
    #    return $clean[$strText];
    #}

    #$key = $strText;

    #// all these tags should be preceeded by a full stop.
    #$fullStopTags = array('li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dd');
    #foreach ($fullStopTags as $tag) {
    #    $strText = str_ireplace('</'.$tag.'>', '.', $strText);
    #}
    #$strText = strip_tags($strText);
    #// Replace commas, hyphens, quotes etc (count them as spaces)
    #$strText = preg_replace('/[",:;()-]/', ' ', $strText);
    #// Unify terminators
    #$strText = preg_replace('/[\.!?]/', '.', $strText);
    #// Add final terminator, just in case it's missing.
    #$strText = trim($strText) . '.';
    #// Replace new lines with spaces
    #$strText = preg_replace('/[ ]*(\n|\r\n|\r)[ ]*/', ' ', $strText);
    #// Check for duplicated terminators
    #$strText = preg_replace('/([\.])[\. ]+/', '$1', $strText);
    #// Pad sentence terminators
    #$strText = trim(preg_replace('/[ ]*([\.])/', '$1 ', $strText));
    #// Remove "words" comprised only of numbers
    #$strText = preg_replace('/ [0-9]+ /', ' ', ' ' . $strText . ' ');
    #// Remove multiple spaces
    #$strText = preg_replace('/[ ]+/', ' ', $strText);
    #// Lower case all words following terminators (for gunning fog score)
    #$strText = preg_replace_callback('/\. [^ ]+/', create_function('$matches', 'return strtolower($matches[0]);'), $strText);

    #$strText = trim($strText);

    #// Cache it and return
    #$clean[$key] = $strText;
    #return text.strip()

_re_count_sentences = re.compile(r'[^\.!?]')
_re_remove_fake_sentences = (
    re.compile(r'[A-Z]\.[A-Z]\.'),
    re.compile(r'Mr\.'),
)
def _count_sentences(text):
    """ Count sentences
    """
    if len(text) == 0:
        return 0

    # Remove "words" such as U.K. and Mr.
    for remover in _re_remove_fake_sentences:
        text = remover.sub('', text)

    return D(max(1, len(_re_count_sentences.sub('', text))))

_re_count_words = re.compile(r'[^ ]')
def _count_words(text):
    """ Count words
    """
    if len(text) == 0:
        return 0

    # Will be tripped by em dashes with spaces either side, among other
    #     similar characters.
    # Space count + 1 is word count.
    return D(1 + len(_re_count_words.sub('', text)))

def average_words_per_sentence(text):
    """ Average words per sentence
    """
    raise Exception("Not implemented")

def _count_syllables(text):
    words = text.split(' ')
    return D(sum(map(syllable_count, words)))

def _count_complex_words(text):
    """ Words with 3 or more syllables
    """

    words = text.split(' ')

    long_words = len(tuple(filter(
        lambda w: _count_syllables(w) >= 3,
        words
    )))

    return D(long_words)/D(len(words))

_re_letters_and_digits = re.compile(r'[^a-zA-Z0-9]')

def _count_letters(text):
    """ Count letters
    """
    text = _re_letters_and_digits.sub('', text)
    return len(text)

_syllable_problem_words = {
    'simile': 3,
    'forever': 3,
    'shoreline': 2,
}

# These syllables would be counted as two but should be one
_sub_syllables = (
    re.compile(r'cial'),
    re.compile(r'tia'),
    re.compile(r'cius'),
    re.compile(r'cious'),
    re.compile(r'giu'),
    re.compile(r'ion'),
    re.compile(r'iou'),
    re.compile(r'sia$'),
    re.compile(r'[^aeiuoyt]{2,}ed$'),
    re.compile(r'.ely$'),
    re.compile(r'[cg]h?e[rsd]?$'),
    re.compile(r'rved?$'),
    re.compile(r'[aeiouy][dt]es?$'),
    re.compile(r'[aeiouy][^aeiouydt]e[rsd]?$'),
    re.compile(r'[aeiouy]rse$'), #Purse, hearse
)

# These syllables would be counted as one but should be two
_add_syllables = (
    re.compile(r'ia'),
    re.compile(r'riet'),
    re.compile(r'dien'),
    re.compile(r'iu'),
    re.compile(r'io'),
    re.compile(r'ii'),
    re.compile(r'[aeiouym]bl$'),
    re.compile(r'[aeiou]{3}'),
    re.compile(r'^mc'),
    re.compile(r'ism$'),
    re.compile(r'([^aeiouy])\1l$'),
    re.compile(r'[^l]lien'),
    re.compile(r'^coa[dglx].'),
    re.compile(r'[^gq]ua[^auieo]'),
    re.compile(r'dnt$'),
    re.compile(r'uity$'),
    re.compile(r'ie(r|st)$'),
)

# Single syllable prefixes and suffixes
_syllable_prefix_suffix = (
    re.compile(r'^un'),
    re.compile(r'^fore'),
    re.compile(r'ly$'),
    re.compile(r'less$'),
    re.compile(r'ful$'),
    re.compile(r'ers?$'),
    re.compile(r'ings?$'),
)

_re_syllable_non_word_chars = re.compile(r'[^a-z]')
_re_syllable_word_parts = re.compile(r'[^aeiouy]+')
def syllable_count(text):
    """ This is not an easy problem to solve:
    https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
        The accepted answer links to a thesis on the problem:
    http://www.tug.org/docs/liang/
    """

    if len(text) == 0:
        return 0

    # We don't care about case, we can assume lowercase for everything make
    # it easier
    text = text.lower()

    # Remove all non alpha characters
    text = _re_letters_and_digits.sub('', text)

    syllable_count_index = 0

    # Specific common exceptions that don't follow the rule set below are
    # handled individually array of problem words (with word as key, syllable
    # count as value)
    if text in _syllable_problem_words:
        return _syllable_problem_words[text]

    # Remove prefixes and suffixes and count how many were taken
    # Interestingly this is a longer piece of code than the PHP version
    prefix_suffix_count = 0
    for pf in _syllable_prefix_suffix:
        prefix_suffix_count += len(pf.findall(text))
        text = pf.sub('', text)

    # Remove non-word characters from word
    text = _re_syllable_non_word_chars.sub('', text)
    word_parts = _re_syllable_word_parts.split(text)

    word_part_count = 0
    for word_part in word_parts:
        if word_part != '':
            word_part_count += 1

    # Some syllables do not follow normal rules
    syllable_count_index = word_part_count + prefix_suffix_count
    for re_syllable in _sub_syllables:
        if re_syllable.search(text):
            syllable_count_index -= 1

    for re_syllable in _add_syllables:
        if re_syllable.search(text):
            syllable_count_index += 1

    if syllable_count_index == 0:
        syllable_count_index = 1

    return D(syllable_count_index)

if __name__ == '__main__':
    sentence = sys.argv[1]
    print(automated_readability_index(sentence))


# Below ported version of Counter added in collections module in Python 2.7
# so that it runs on Python 2.5 or later.
# Recipe taken from
# http://code.activestate.com/recipes/576611-counter-class/
#
# Original Counter code for Python 2.7 is
# http://docs.python.org/dev/library/collections.html#counter-objects
#


from operator import itemgetter
from heapq import nlargest
from itertools import repeat, ifilter

class Counter(dict):
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        """ Get from keys
        """
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    # fast path when counter is empty
                    dict.update(self, iterable)
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        """ Like dict.copy() but returns a Counter instance instead of a dict.
        """
        return Counter(self)

    def __delitem__(self, elem):
        """ Like dict.__delitem__() but does not raise KeyError for
            missing values.
        """
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


if __name__ == '__main__':
    import doctest
    print doctest.testmod()
