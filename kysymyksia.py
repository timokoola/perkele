#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import sqlite3
import time

import random
from twython import TwythonStreamer
from twython import Twython
from twython.exceptions import TwythonError
import re
from tweet_parse_utils import *
import nltk

keyfile = "kysymyksia.keys"
me = "kysymysvastaus"
api = None

questions = [u"mitä", u"onko", u"eikö", u"miksi", u"haluatko", u"haluaako", u"missä", u"kuka", u"kenen", u"kenet",
             u"mikä", u"pitäisikö", u"enkö", u"voiko", u"saako"]

conn = sqlite3.connect('kysymystweets.db')
r = random.Random()


def save_tweet_db(tweet, summary):
    c = conn.cursor()
    row = ("%f" % time.time(), json.dumps(tweet), tweet["user"]["id"], summary)
    c.execute('INSERT INTO questions VALUES (NULL,?,?,?,?)', row)
    conn.commit()


class TwythonHelper:
    def __init__(self, keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        self.consumerkey = lines[0].split("#")[0]
        self.consumersecret = lines[1].split("#")[0]
        self.accesstoken = lines[2].split("#")[0]
        self.accesssec = lines[3].split("#")[0]

        self.api = Twython(self.consumerkey, self.consumersecret, self.accesstoken, self.accesssec)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            if "lang" in data:
                if data["lang"] != "fi":
                    return

            info = data.get("extended_tweet", data)

            fulltext = info.get("full_text", info.get("text"))
            if "?" not in fulltext:
                return
            if fulltext.startswith("RT"):
                return
            if data["user"]["screen_name"] == me:
                return

            indices = get_entity_indice_list(info["entities"])

            clipped = strip_by_indices(fulltext, indices)
            clipped = fix_html_entities(clipped)
            if len(fulltext) > 2 and fulltext[1] == '@':
                clipped = clipped[2:]

            comp = clipped.lower()
            if not any(w in comp for w in questions):
                pass
            else:
                try:
                    tokenizer = nltk.data.load('tokenizers/punkt/finnish.pickle')
                    sentences = tokenizer.tokenize(clipped.strip())
                    # api.update_status(status=clipped)
                    for s in sentences:
                        if s.endswith("?"):
                            save_tweet_db(data, s)
                        if r.random() < 0.07 and len(s) > 5:
                            api.update_status(status=s)
                except TwythonError:
                    pass

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


if __name__ == '__main__':
    helper = (TwythonHelper(keyfile))
    api = helper.api
    me = api.get_account_settings()["screen_name"]
    stream = MyStreamer(helper.consumerkey, helper.consumersecret,
                        helper.accesstoken, helper.accesssec)
    track_items = u",".join([x for x in questions])
    stream.statuses.filter(track=track_items)
