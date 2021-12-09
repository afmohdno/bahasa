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
dip = rules["diphthongs"]
non = rules["non_first"]
all_letter = con + vow

def syllable_generator(pattern):
	sequence = []
	last = ""
	for letter in pattern:
		if letter is "c":
			sequence.extend(random.choice(con))
		elif letter is "v":
			if last in vow:
				sequence.extend(random.choice(dip[last]))
			else:
				sequence.extend(random.choice(vow))
		elif letter is "d":
			sequence.extend(random.choice(dip))
		last = sequence[-1]
		print sequence, last, 41
		if last in non:
			sequence.clear()
			sequence.extend(random.choice(vow))

	syllable = "".join(sequence)

	print sequence, 41

	return syllable

def word_generator(i):
	pattern = ""
	one_syllable_pattern = ["v","cv","cvc","cd","cdc"]
	two_syllable_pattern = ["cvv","cvcv","cvvc","cvccvc","cvcvc","cdcvc","dc","vnv","vccv","vcvc"]

	if i == 1:
		pattern = random.choice(one_syllable_pattern)
	elif i == 2:
		pattern = random.choice(two_syllable_pattern)

	print pattern, 55
	word = syllable_generator(pattern)
	return word

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

	syllable = syllable_generator("cvvcvc")
	word = word_generator(2)
	print syllable, 77

	data["sound"] = c0+v0
	data["syllable"] = syllable
	data["word"] = word

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