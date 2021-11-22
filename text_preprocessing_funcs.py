import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import en_core_web_sm



nlp = spacy.load('en_core_web_sm') # load model

# STOPWORDS = list(STOP_WORDS)
# contraction_mapping = {"don't":"do not", "can't": "cannot", "ain't": "is not", "aren't": "are not"}
POS_TAGS = ['PROPN', 'ADJ', 'NOUN', 'VERB']

extra_words = list(STOP_WORDS)+list(punctuation)+['\n']  # words and punctuations to be ignored



def generate_summary(txt, txt_percentage):

	# txt = txt.lower() # Make all letters lowercase
	text = nlp(txt) 

	all_words = [word.text for word in text]


	freq_word = {}   # dict with key:word, value: number of occurancies
	for w in all_words:

		w1 = w.lower()
		if w1 not in extra_words and w1.isalpha():  # filter certain words

			if w1 in freq_word.keys():
				freq_word[w1] += 1
			else:
				freq_word[w1] = 1

	""" 
	Generate a tiny summary based on most important words -> title
	Word Importance -> fewer occurancies
	title will not be used in the final implementation or as a response value from the API (just for fun)
	"""
	txt_title = ""
	sorted_words = sorted(freq_word.values())
	max_freq = sorted_words[-3:]  # Get 4 most important words

	for word, freq in freq_word.items():  
	    
		if freq in max_freq:
			txt_title += word + " "
		else:
			continue


	for word in freq_word.keys():  
		freq_word[word] = (freq_word[word]/max_freq[-1])

	sent_strength = {} # dict with most valuable sentences

	for sent in text.sents:  # iterate through sentences
		for word in sent:
	       
			if word.text.lower() in freq_word.keys():
	            
				if sent in sent_strength.keys():
					sent_strength[sent]+=freq_word[word.text.lower()]
				else:
					sent_strength[sent]=freq_word[word.text.lower()]
			else:
				continue

	top_sentences = (sorted(sent_strength.values())[::-1])  # sort top sentences

	topX_sentences = int(txt_percentage*len(top_sentences))  # Get x% of most important sentences in the document
	top_sent = top_sentences[:topX_sentences]

	"""
	Generate the summary with the x% most valuable sentences in the given document
	this way the end result will be Readable
	"""
	
	txt_summary = ""
	for sent,strength in sent_strength.items():  
		if strength in top_sent:
			txt_summary += str(sent) + "," 
		else:
			continue

	return txt_title, txt_summary


""" -------- Depricated --------

def text_preprocessing(text):

	keywords = []

	txt = text.lower() # Make all letters lowercase
	text = nlp(text)

	for token.pos_ in POS_TAGS:
		if token.text in STOPWORDS:
			keywords.append(token)


			
	return txt

"""