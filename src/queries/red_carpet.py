import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams
from src.helpers.find import find_name

# golden globes stopwords
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']

#best dressed words
best_dressed_sw = ['best','dressed','also','red','carpet','redcarpet','looks','dress','best-dressed','worst-dressed','one','call','tonight','damn','men','women','love','beautifully','sexy','eonline','soon','thanks','obsessed','putting','list','thank']
best_list = ['best','beautiful','pretty','love','sexy','beautifully']

#worst dressed words
worst_dressed_sw = ['best','worst','dressed','also','red','carpet','redcarpet','looks','dress','best-dressed','worst-dressed','one','call','tonight','damn','men','women','love','beautifully','sexy','eonline','soon','thanks','obsessed','putting','list','thank']
worst_list = ['ugly','hate','awful','terrible','worst','sucks','not','isnt']
# red carpet keywords
best_dressed_kw = []
worst_dressed_kw = []
bdl = []
wdl = []


def find_best_dressed(data, year):
	best_dressed_dict = {}
	for obj in data:
		if 'dress' in obj['text']:
			if any(x in obj['text'] for x in worst_list):
				continue
			else:
				if any(x in obj['text'] for x in best_list):
			#for sw in best_list:
				#if sw in obj['text']:
			#tokens = nltk.word_tokenize(obj['text'])
					tokens = bigrams(nltk.word_tokenize(obj['text']), best_dressed_kw, gg_sw + best_dressed_sw+best_list)
					for tkn in tokens:
						tkn = tkn.lower()
						if tkn not in best_dressed_dict:
							best_dressed_dict[tkn] = 1
						else:
							best_dressed_dict[tkn] += 1
	best_dressed_lst = sorted(best_dressed_dict.items(), key=lambda x: x[1], reverse=True)
	#best_dressed_lst = find_name(best_dressed_lst,best_dressed_dict)
	return best_dressed_lst

def find_worst_dressed(data, year):
	worst_dressed_dict = {}
	for obj in data:
		if 'dress' in obj['text']:
			for sw in worst_list:
				if sw in obj['text']:
		#tokens = nltk.word_tokenize(obj['text'])
					tokens = bigrams(nltk.word_tokenize(obj['text']), worst_dressed_kw, gg_sw + worst_dressed_sw)
					for tkn in tokens:
						tkn = tkn.lower()
						if tkn not in worst_dressed_dict:
							worst_dressed_dict[tkn] = 1
						else:
							worst_dressed_dict[tkn] += 1
	worst_dressed_lst = sorted(worst_dressed_dict.items(), key=lambda x: x[1], reverse=True)
	#best_dressed_lst = find_name(best_dressed_lst,best_dressed_dict)
	bd = find_best_dressed(data,year)
	for item in bd:
		if item[1]>35:
			bdl.append(item[0])
	for item in worst_dressed_lst:
		if item[0] in bdl:
			pass
		else:
			wdl.append(item)
	return wdl