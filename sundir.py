import astral
# -*- coding: utf-8 -*-
import datetime
import pytz
from twython import Twython


model = """Aurinko %s\nAurinko %s.\nAuringon suunta %d astetta ja korkeus %d astetta."""
now = datetime.datetime.now(tz=pytz.timezone("Europe/Helsinki"))
tomorrow = datetime.datetime.now(tz=pytz.timezone("Europe/Helsinki")) + datetime.timedelta(1)

class TwythonHelper:

    def __init__(self, keyfile):
        f = open(keyfile)
        lines = f.readlines()
        f.close()
        consumerkey = lines[0].split("#")[0]
        consumersecret = lines[1].split("#")[0]
        accesstoken = lines[2].split("#")[0]
        accesssec = lines[3].split("#")[0]

        self.api = Twython(consumerkey, consumersecret, accesstoken, accesssec)

def helsinki_sun():
	a = astral.Astral()
	a.solar_depression = "civil"
	return a["Helsinki"]

def sunrise_string(sun):
	timestr = "%d.%02d" % (sun.sunrise().time().hour, sun.sunrise().time().minute)
	if sun.sunset() < now:
		tsun = helsinki_sun().sun(tomorrow)["sunrise"]
		timestr = "%d.%02d" % (tsun.time().hour, tsun.time().minute)
		return "Aurinko nousee huomenna %s." % timestr
	elif sun.sunrise() > now:
		return "Aurinko nousee %s." % timestr
	else:
		return "Aurinko nousi %s." % timestr

def sunset_string(sun):
	timestr = "%d.%02d" % (sun.sunset().time().hour, sun.sunset().time().minute)
	if sun.sunset() > now:
		return "Aurinko laskee %s." % timestr
	else:
		return "Aurinko laski %s." % timestr

def sundir_str(sun):
	elev = int(sun.solar_elevation())
	az = int(sun.solar_azimuth())
	if elev < 0:
		return "Aurinko on ilmansuunnassa %d ja %d astetta horisontin alapuolella." % (az,elev)
	else:
		return "Aurinko on ilmansuunnassa %d ja %d astetta horisontin yläpuolella." % (az,elev)

if __name__ == '__main__':
	sun = helsinki_sun()
	tweet =  "\n".join([sunrise_string(sun), sunset_string(sun), sundir_str(sun)])
	print tweet, len(tweet)
	api = (TwythonHelper("test.keys")).api
	api.update_status(status=tweet)
