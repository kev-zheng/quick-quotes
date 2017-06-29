import sys
sys.path.append('lib')

import logging
import json
import random

import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

quote_file = open('quotable.json', 'r').read()
data = json.loads(quote_file)

def make_message(quote, author):
	val = random.randint(0, 2)
	if val == 0:
		return '{} once said {}'.format(author, quote)
	else:
		return '{} <break time="500ms"/> {}'.format(quote, author)

@ask.launch

@ask.intent('RandomQuoteIntent')
def random_quote():
    author = random.choice(list(data.keys()))
    quote = random.choice(data[author])
    return statement(make_message(quote, author))

@ask.intent('AuthorQuoteIntent')
def author_quote(author):
	quote = random.choice(data[author])
	return statement(make_message(quote, author))

if __name__ == '__main__':
    app.run(debug=True)