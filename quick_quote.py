from __future__ import print_function

import os
import json
import random

file = open('quick_quote.json').read()
data = json.loads(file)

# Lowercase for better comparisons
synonym_info = {k.lower():v for k, v in data['Synonyms'].items()}
author_info = [x.lower() for x in data['Authors']]

quote_info = data['Quotes']

SKILL_ID = '57dd0312-3b08-4970-a91c-ac65f880874c'

def lambda_handler(event, context):

    # Verifying correct request
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.{}".format(SKILL_ID)):
         raise ValueError("Invalid Application ID")

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    return None

def on_launch(launch_request, session):
    """ Gives a random quote if user does not specify anything"""
    return random_quote()
    
def on_intent(intent_request, session):
    """Handles different types of intents"""
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "RandomQuoteIntent":
        return random_quote()
    elif intent_name == "AuthorQuoteIntent":
        return author_quote(intent, session)
    else:
        raise ValueError("Invalid intent")

# --------------- Functions that control the skill's behavior ------------------
def pair_quote(quote, author):
    """Pairs a quote with its author"""
    val = random.randint(0, 2)
    if val == 0:
        return '{} once said, {}'.format(author, quote)
    else:
        return '{} <break time="500ms"/> {}'.format(quote, author)

def random_quote():
    session_attributes = {}
    card_title = 'Random Quote'

    author = random.choice(list(quote_info.keys()))
    quote = random.choice(quote_info[author])

    speech_output = pair_quote(quote, author)
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, should_end_session))

def author_quote(intent, session):
    session_attributes = {}
    should_end_session = False
    author = intent['slots']['author']['value']
    card_title = '{} Quote'.format(author)

    if author.lower() not in author_info and author.lower() not in synonym_info.keys():
        speech_output = """Sorry, I don't have a quote for {}. I can give a quote for an author's specific full name or last name like Abraham Lincoln or Lincoln. Who would you like me to quote?""".format(author)
        should_end_session = False
    else:
        # Convert back to full author if it is a synonym
        if author.lower() in synonym_info.keys():
            author = synonym_info[author.lower()]
        quote = random.choice(quote_info[author])
        speech_output = pair_quote(quote, author)
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, should_end_session))


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': ''
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
