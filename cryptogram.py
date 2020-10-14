import string
import random
import urllib.request as r
import time as t
from html.parser import HTMLParser


class TheHTMLParser(HTMLParser):
    _ptag = False
    quotes = list()
    _current_quote = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for key, val in attrs:
                if key == 'class' and val.startswith('st'):
                    self._ptag = True

    def handle_data(self, data):
        if self._ptag:
            self._current_quote += data

    def handle_endtag(self, tag):
        if tag == 'p':
            self._ptag = False
            if self._current_quote != '':
                self.quotes.append(self._current_quote)
                self._current_quote = ''


def generate_quote():
    url = 'http://www.smart-words.org/quotes-sayings/famous-one-liners.html'
    parser = TheHTMLParser()
    with r.urlopen(url) as f:
        a = list(line.decode("utf-8").strip() for line in f.readlines())

    for eachline in a:
        parser.feed(eachline)
    return random.choice(parser.quotes).upper()


class Cryptogram:
    @property
    def num_guessed(self):
        return len([i for i in self.guessed_quote if i != ''])

    def __init__(self):
        self.quote = generate_quote()
        self.quote_letters = list(self.quote)
        self.guessed_quote = list()
        self.encoded_quote = list()
        self.guesses = dict()
        self.start_time = round(t.time())
        self.code = {}
        self.get_code()
        self.encode_quote()
        self.generate_guesses()

    def encode_quote(self):
        for j in self.quote_letters:
            try:
                self.encoded_quote.append(self.code[j])
            except KeyError:
                self.encoded_quote.append(j)

    def generate_guesses(self):
        for i in self.encoded_quote:
            if i.isalpha():
                self.guesses[i] = ''
                self.guessed_quote.append('')
            else:
                self.guesses[i] = i
                self.guessed_quote.append(i)

    def get_code(self):
        alphabet = list(string.ascii_uppercase)
        shuffled_alphabet = list(string.ascii_uppercase)
        random.shuffle(shuffled_alphabet)
        length = len(alphabet)
        for i in range(length):
            self.code[alphabet[i]] = shuffled_alphabet[i]

    def guess_letter(self, old_letter, new_letter):
        try:
            self.guesses[old_letter] = new_letter
            self._replace_guesses()
        except KeyError:
            pass

    def _replace_guesses(self):
        for i in range(len(self.quote_letters)):
            self.guessed_quote[i] = self.guesses[self.encoded_quote[i]]

    def check_win(self):
        return self.guessed_quote == self.quote_letters

