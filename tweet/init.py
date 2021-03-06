from flask import Flask, render_template, request, jsonify

import modules.tweet_dumper as tweet_dumper
import modules.maxentclassifier as mcf
import modules.answer as naive
import modules.twitter_data_stream as tds
import modules.tags_count as tc
import time

app = Flask(__name__)

word = ""

country_names = {"india" : "India","pakistan" : "Pakistan","usa":"USA","uk":"UK"}

#Renders the home page of the application server.
@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/test')
def test():
	return render_template('result.html')

@app.route('/world')
def world():
	return render_template('world.html')




@app.route('/naive_classifier')
@app.route('/naive_classifier/<new_word>')
def naive_classifier(new_word=None):	
	global word
	if new_word:
		word = new_word
	(positive, negative, neutral) = naive.main(word)
	total = positive + negative + neutral
	pos_percent = (100.0*positive/total)
	neg_percent = (100.0*negative/total)
	neu_percent = (100.0*neutral/total)
	return render_template('result.html', positive="{:.2f}".format(pos_percent) , negative="{:.2f}".format(neg_percent), neutral="{:.2f}".format(neu_percent))

@app.route('/max_classifier')
@app.route('/max_classifier/<new_word>')
def max_classifier(new_word=None):
	global word
	if new_word:
		word = new_word
	(positive, negative, neutral) = mcf.main(word)
	pos_percent = (100.0*positive/(positive + negative))
	neg_percent = 100 - pos_percent
	return render_template('result.html', positive="{:.2f}".format(pos_percent) , negative="{:.2f}".format(neg_percent))






@app.route('/naive_classifier_world')
@app.route('/naive_classifier_world/<new_word>')
def naive_classifier_world(new_word=None):	
	global word
	country_one = None
	country_two = None
	if new_word:
		arr = new_word.split('_')
		word = arr[0]
		country_one = arr[1]
		country_two = arr[2]

	(positive1, negative1, neutral1) = naive.main(word + '_' + country_one)
	total1 = positive1 + negative1 + neutral1
	pos_percent1 = (100.0*positive1/total1)
	neg_percent1 = (100.0*negative1/total1)
	neu_percent1 = (100.0*neutral1/total1)

	(positive2, negative2, neutral2) = naive.main(word + '_' + country_two)
	total2 = positive2 + negative2 + neutral2
	pos_percent2 = (100.0*positive2/total2)
	neg_percent2 = (100.0*negative2/total2)
	neu_percent2 = (100.0*neutral2/total2)


	return render_template('result_country.html',\
		positive1="{:.2f}".format(pos_percent1),\
		negative1="{:.2f}".format(neg_percent1),\
	 	neutral1="{:.2f}".format(neu_percent1),\
	 	positive2="{:.2f}".format(pos_percent2),\
	 	negative2="{:.2f}".format(neg_percent2),\
	 	neutral2="{:.2f}".format(neu_percent2),\
	 	country_one=country_names[country_one],\
	 	country_two=country_names[country_two]
	 )

@app.route('/max_classifier_world')
@app.route('/max_classifier_world/<new_word>')
def max_classifier_world(new_word=None):
	global word
	country_one = None
	country_two = None
	if new_word:
		arr = new_word.split('_')
		word = arr[0]
		country_one = arr[1]
		country_two = arr[2]

	(positive1, negative1, neutral1) = mcf.main(word + '_' + country_one)
	pos_percent1 = (100.0*positive1/(positive1 + negative1))
	neg_percent1 = 100 - pos_percent1

	(positive2, negative2, neutral2) = mcf.main(word + '_' + country_two)
	pos_percent2 = (100.0*positive2/(positive2 + negative2))
	neg_percent2 = 100 - pos_percent2


	return render_template('result_country.html',\
		positive1="{:.2f}".format(pos_percent1),\
		negative1="{:.2f}".format(neg_percent1),\
		positive2="{:.2f}".format(pos_percent2),\
		negative2="{:.2f}".format(neg_percent2),\
	 	country_one=country_names[country_one],\
	 	country_two=country_names[country_two]
	 	)

@app.route('/evaluate')
def evaluate():
	global word
	word = request.args.get('word')
	print "Fetching tweets for ", word
	tweet_dumper.get_all_tweets(word)
	# import time
	# time.sleep(2)
	print "Completed"
	return jsonify(result="Fetching tweets")

@app.route('/fetch_country_data/<country_name>')
def fetch_country_data(country_name=None):
	global word
	word = request.args.get('word')
	word = word + "_" + country_name
	print "Fetching country tweets for ", word

	tweet_dumper.get_all_tweets(word)
	# import time
	# time.sleep(2)
	print "Completed"
	return jsonify(result="Fetching tweets")

	"""cord1, cord2 = None, None
	if country_name == 'india':
		cord1 = ["-18.5204", "73.8567"]
		cord2 = ["-22.5726", "88.3639"]
	elif country_name == 'pakistan':
		cord1 = ["26.7303", "64.1478"]
		cord2 = ["-31.5546", "74.3572"]
	elif country_name == 'usa':
		cord1 = ["-18.5204", "73.8567"]
		cord2 = ["-36.1699", "115.1398"]
	else:
		cord1 = ["-51.4545", "2.5879"]
		cord2 = ["-54.6917", "1.2129"]

	print "Fetching %s[%s]"%(word, country_name)
	tds.fetchsamples(word, cord1, cord2, country_name)
	print "Fetched all data"
	print "Parsing JSON file"
	tc.parse_data(word, country_name)
	print "Parsing completed"

	print "All Operations completed"
	return jsonify(result="Fetching tweets")"""

if __name__ == "__main__":
	app.debug = True
	app.run('', port=4000)
