from bottle import *
from datetime import datetime
import random
import json

application = default_app()
title = "bahasa"
meta = {
	"year" : 2021,
	"company" : "bahasa"
}

with open('data/users.json') as file:
	userdata = json.load(file)
users = userdata
session = users[0]

with open('data/rules.json') as file:
	bahasa_rules = json.load(file)
rules = bahasa_rules

con = rules["consonants"]
vow = rules["vowels"]
dip_d = rules["diphthongs_dict"]
dip_b = rules["diphthongs_between"]
dip_e = rules["diphthongs_end"]
dip_l = dip_b + dip_e
non_l = rules["non_last"]
nas = rules["nasal"]
plo = rules["plosive"]
afr = rules["africative"]
s_structure = rules["syllable_structure"]
non_plo = []
for each in con:
	if each not in plo: non_plo.append(each)
non_nas = []
for each in nas:
	if each not in nas: non_nas.append(each)
non_last = []
for each in con:
	if each not in non_l: non_last.append(each)
non_c_c = []
for each in con:
	if each not in rules["non_cf"]: non_c_c.append(each)
p_a = plo + afr
all_letter = con + vow

# usually kata dasar only have 2 or 3 syllables
def syllable_constructor():
	pattern = []
	data = s_structure
	while isinstance(data,dict):
		if isinstance(data,list):
			print data, "list data"
			if data != []:
				last = random.choice(data)
				pattern.append(last)
		else:
			order = data.keys()
			last = random.choice(order)
			pattern.append(last)
			data = data[last]
	p = str("".join(pattern))
	return syllable_generator(p)

def syllable_generator(pattern):
	sequence = []
	print pattern, type(pattern)
	last = ""
	store = ""
	for letter in pattern:
		if sequence == []:
			print "first letter"
			if letter is "v":
				last = "a"
			elif letter is "c":
				last = random.choice(con)
		elif len(sequence) == (len(pattern)-1):
			print "last letter"
			if letter is "c":
				last = random.choice(non_last)
				if last == "y":
					last = "i"
				elif last == "w":
					last = "u"
			elif letter is "v":
				if last in vow:
					last = random.choice(dip_d[last])
				else:
					last = random.choice(vow)
			elif letter is "d":
				last = random.choice(dip_l)
		else:
			if letter is "c":
				if last in con:
					while last == sequence[-1]:
						if last in nas:
							last = random.choice(plo)
						elif last in plo:
							last = random.choice(non_plo)
						else:
							last = random.choice(non_c_c)
				elif last in vow:
					last = random.choice(con)
					if last == "y":
						last = "i"
					elif last == "w":
						last = "u"
				else:
					last = random.choice(con)
			elif letter is "v":
				if last in vow:
					if dip_d[last] != "": # e never followed by any other vowels
						last = random.choice(dip_d[last]) # only use possible v+v arrangements
				else:
					last = random.choice(vow)
			elif letter is "d":
				last = random.choice(dip_b)
		print len(sequence),":",last
		sequence.append(last)
	syllable = "".join(sequence)

	print sequence, 52

	return syllable

# Define an handler for the root URL of our application.
@route('/')
def main():
	return template("views/index.html", title=title, meta=meta)

@route('/landing')
def main():
	return template("views/landing.html", title=title, meta=meta)

@route('/generator')
def main():
	data = {}

	c0 = random.choice(con)
	v0 = random.choice(vow)

	word1 = syllable_constructor()
	word2 = syllable_constructor()
	word3 = syllable_constructor()
	data["sound"] = c0+v0
	data["word"] = [word1,word2,word3]


	return template("views/generator.html", title=title, meta=meta, data=data)

@route('/profile/<profile_url>')
def profile(profile_url):
	user_exist = False
	user_profile = {}
	for user in users:
		if user["user_url"] == profile_url:
			user_exist = True
			user_profile = user

	if user_exist:
		return template("views/profile.html", title=title + " | Profile")
	else:
		return 'Sorry, Nothing at this URL.'

@route('/favicon.ico')
def get_favicon():
    return server_static('favicon.ico')

# Define an handler for 404 errors.
@error(404)
def error_404(error):
	"""Return a custom 404 error."""
	return 'Sorry, Nothing at this URL.'

# Define an handler for 500 errors.
@error(500)
def error_500(error):
	"""Return a custom 500 error."""
	return "Sorry, couldn't connect to server ."

# specifying the path for the files
@route('/<filepath:path>')
@route('/profile/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='./static/')

if __name__ == '__main__':
    application.run(reloader=True, host="0.0.0.0", port=int(os.environ.get("PORT", 2222)))