from random import choice

from markov_babbler.settings import *


class NGram():
    def __init__(self):
        self.token = ''
        self.followers = {}

    def get_token(self):
        return self.token

    def get_followers(self):
        return self.followers


def babble(texts, n=3, num_of_words=50):
    # Make sure that we provide sane defaults for values
    n, num_of_words = sanitize_input(n, num_of_words)

    if texts:
        tokens = tokenize(texts)
        n_grams = create_n_grams(tokens, n)
        result = create_babble(n_grams, num_of_words)

    else:
        result = 'ERR: No texts to babble from were found'

    return result


def sanitize_input(n, num_of_words):
    if num_of_words > 1000:
        num_of_words = 1000

    if n < 2:
        n = 2
    elif n > MAX_N:
        n = MAX_N
    return n, num_of_words


def create_n_grams(tokens, n):
    n_grams = {}
    index = 0
    for token in tokens:
        token_gram = []

        for i in range(1, n, 1):

            if index+i < len(tokens):  # avoid index out of range at end of list
                token_gram.append(tokens[index+i])

        if len(token_gram) == n - 1:  # make sure there is a full n-gram before using it
            if not token in n_grams:
                n_gram = NGram()
                n_gram.token = token
                n_gram.followers[index] = token_gram
                n_grams[token] = n_gram

            else:
                n_grams[token].followers[index] = token_gram

        index += 1

    return n_grams


def tokenize(texts):
    tokens = []
    for text in texts:
        tokens += text.split()

    return tokens


def create_babble(n_grams, num_of_words):
    # make the babble
    next_token_key = choice(list(n_grams.keys()))
    next_token = n_grams[next_token_key]
    final_babble = u'%s ' % next_token.get_token()
    i = 0
    while i <= num_of_words:
        follower_choice_index = choice(list(next_token.get_followers().keys()))

        for follower in next_token.get_followers()[follower_choice_index]:
            i += 1
            final_babble += u'%s ' % follower
            try:  # every once in a while, such as with the key u'not', a KeyError will present itself
                next_token = n_grams[follower]
            except KeyError:
                next_token = n_grams[choice(list(n_grams.keys()))]

    return final_babble