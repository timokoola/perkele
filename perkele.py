#!/usr/bin/python
from twython import TwythonStreamer
from twython import Twython
from twython.exceptions import TwythonError
import re
import pprint
import sqlite3
import time
import json
import random
from tweet_parse_utils import *


conn = sqlite3.connect('tweets.db')
r = random.Random()


keyfile = "prklsuomi.keys"
me = 3075601787
api = None
track_words = ['perkele', 'vittu', 'saatana', 'vitun', 'saatanan',
               'perkeleen', 'jumalauta', 'paska']


def save_tweet_db(tweet):
    c = conn.cursor()
    row = ("%f" % time.time(), json.dumps(tweet), tweet["user"]["id"], tweet["text"])
    c.execute('INSERT INTO tweets VALUES (?,?,?,?)', row)
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
            info = data.get("extended_tweet", data)

            fulltext = info.get("full_text", info.get("text"))
            if fulltext.startswith("RT"):
                print "RT, skipped"
                return
            if data["user"]["id"] == me:
                print "My own tweet"
                return
            save_tweet_db(data)
            if data["lang"] != "fi":
                print "Ei suomea"
                return

            indices = get_entity_indice_list(info["entities"])

            clipped = strip_by_indices(fulltext, indices)
            clipped = fix_html_entities(clipped)
            if len(fulltext) > 2 and fulltext[1] == '@':
                clipped = clipped[2:]

            comp = clipped.lower()
            if not any(w in comp for w in track_words):
                print "No track words in clipped tweet\n"
                return

            try:
                if r.random() < 0.1:
                    api.update_status(status=clipped)
                else:
                    print "Skipped tweeting randomly."
            except TwythonError:
                print "Duplicate"

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


if __name__ == '__main__':
    helper = (TwythonHelper(keyfile))
    api = helper.api
    stream = MyStreamer(helper.consumerkey, helper.consumersecret,
                    helper.accesstoken, helper.accesssec)
    stream.statuses.filter(track=','.join(track_words))
