import astral
# -*- coding: utf-8 -*-

def helsinki_sun():
	a = astral.Astral()
	a.solar_depression = "civil"
	return a["Helsinki"]

perus = [u"vittu", u"saatana", u"perkele", u"jumalauta", u""]
gen = [u"vitun", u"saatanan", u"perkeleen", u"" ]

aamuhamara = [u"PERUSPISTE GENPILKKU aamuhämärä alkoi just. PERUS", u"PERUSPILKKU nyt alkoi sarastaa."]
auringonnousu = [u"PERUSPILKKU nyt se GEN aurinko nousi. PERUS", u"Taas se GEN aurinko nousee.", u"PERUSPILKKU nyt luulisi näkevän jo jotain. PERUSPISTE"]
auringonlasku = [u"Auringonlasku. PERUS", u"GEN auringonlasku. PERUSPISTE", u"PERUSPILKKU nyt tuli hämärää. PERUSPISTE"]

if __name__ == '__main__':
	sun = helsinki_sun()

	