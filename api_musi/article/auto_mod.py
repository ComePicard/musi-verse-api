import re
from os import listdir

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator

from api_musi.article import MODERATION_VAL

file = open(r"../sources/banwords.txt").readlines()
banwords = []
for line in file:
    banwords.append(line.strip())


def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text


def is_toxic(comment):
    translated_comment = translate_text(comment, 'fr', 'en')

    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(translated_comment)
    print("Scores de sentiment :", sentiment_scores)

    if sentiment_scores['compound'] < MODERATION_VAL:
        return True
    else:
        return False


def is_ban_word(comment):
    for banw in banwords:
        if banw in comment.lower():
            return True
    return False


def is_spam(comment):
    repetitive_pattern = re.compile(r'(.)\1{2,}', re.IGNORECASE)
    if repetitive_pattern.search(comment):
        return True

    capital_pattern = re.compile(r'\b[A-Z]{2,}\b')
    if capital_pattern.search(comment):
        return True

    return False
