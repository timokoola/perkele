#!/usr/bin/python
from twython import TwythonStreamer
from twython import Twython
from twython.exceptions import TwythonError
import re

keyfile = "enmutta.keys"
me = "enmutta"
api = None
ats = re.compile("@\w+")
url = re.compile("http://\S+")
risu = re.compile("#\S+")

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
            fulltext = data["text"]
            if fulltext.startswith("RT"):
                print "RT, skipped"
                return
            if data["user"]["screen_name"] == me:
                print "My own tweet"
                return
            clipped = ats.sub("",fulltext)
            clipped = url.sub("",clipped)
            clipped = risu.sub("",clipped)
            clipped = clipped.strip()
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
