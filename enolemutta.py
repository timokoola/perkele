#!/usr/bin/python
from twython import TwythonStreamer
from twython import Twython
from twython.exceptions import TwythonError
import re
from tweet_parse_utils import *
 

keyfile = "enmutta.keys"
me = "enmutta"
api = None


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
            if data["user"]["screen_name"] == me:
                print "My own tweet"
                return

            indices = get_entity_indice_list(info["entities"])

            clipped = strip_by_indices(fulltext, indices)
            clipped = fix_html_entities(clipped)
            if len(fulltext) > 2 and fulltext[1] == '@':
                clipped = clipped[2:]

            comp = clipped.lower()
            order = [comp.find(x) for x in ["en", "ole", "mutta"]]
            if sorted(order) == order and -1 not in order:
                try:
                    api.update_status(status=clipped)
                except TwythonError:
                    print "Duplicate"
            else:
                print "Not in order skipped"

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


if __name__ == '__main__':
    helper = (TwythonHelper(keyfile))
    api = helper.api
    me = api.get_account_settings()["screen_name"]
    stream = MyStreamer(helper.consumerkey, helper.consumersecret,
                    helper.accesstoken, helper.accesssec)
    stream.statuses.filter(track='en ole mutta')
