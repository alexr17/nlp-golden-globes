import nltk
from src.helpers.load import load_json
from src.helpers.clean import valid_tkn, bigrams
from src.helpers.find import find_name


#golden globes stopwords
gg_sw = ['golden', 'globes', 'goldenglobes', 'globe']

#funny jokes words
funny_list = ['hilarious', 'ha', 'haha', 'lol', 'joke', 'laugh', 'laughing', 'LOL', 'I\'m dead']

funniest_jokes_kw = []

names = set(line.strip() for line in open('././data/names.txt'))
titles = set(line.strip() for line in open('././data/titles.txt'))

#finidng best jokes
def find_jokes(data):
    funny_jokes_dict = {}
    for obj in data:
        if '\"' in obj['text']:
            #getting index range where joke is quoted
            start_quote_index = obj['text'].find('\"')
            end_quote_index = obj['text'].find('\"', start_quote_index +1)

            #checking the quote is not a movie title
            if obj['text'][start_quote_index+1:end_quote_index] not in titles:
                if start_quote_index != -1 and end_quote_index != -1:
                    tweet_without_quote = obj['text'][:start_quote_index]+obj['text'][end_quote_index+1:]
                    tokens1 = nltk.word_tokenize(tweet_without_quote)
                    funny_words = -1
                    #checking for funny keywords in the tweet excluding the quote
                    for i in range(len(tokens1)):
                        if tokens1[i] in funny_list:
                            if funny_words != -1:
                                funny_words += 1
                            else:
                                funny_words = 1
                    if funny_words != -1:
                        tokens = bigrams(nltk.word_tokenize(tweet_without_quote), funniest_jokes_kw, gg_sw + funny_list)
                        for tkn in tokens:
                            tkn = tkn.lower()
                            #check that there is a name of a celebrity who made the joke
                            if tkn in names:
                                if obj['text'][start_quote_index:end_quote_index+1] not in funny_jokes_dict:
                                    funny_jokes_dict[obj['text'][start_quote_index:end_quote_index+1]] = [tkn, 1, obj['text']]
                                else:
                                    funny_jokes_dict[obj['text'][start_quote_index:end_quote_index+1]][1] += 1
                                    funny_jokes_dict[obj['text'][start_quote_index:end_quote_index+1]][2] = obj['text']


    jokes_list = sorted(funny_jokes_dict.items(), key=lambda x: x[1][1], reverse=True)
    #printing jokes results
    jokes_dict = {}
    print('Best jokes of the night: \n')
    for i in range(5):
        if i < len(jokes_list):
            if jokes_list[i][1][1]>0:
                if jokes_list[i][1][0] in jokes_dict:
                    jokes_dict[jokes_list[i][1][0]].append(jokes_list[i][0])
                else:
                    jokes_dict[jokes_list[i][1][0]] = [jokes_list[i][0]]
                print ('Celebrity: ' + jokes_list[i][1][0] +'\n'
                       +'Joke: '+ jokes_list[i][0] + '\n'
                       #+'Full tweet: '+ str(jokes_list[i][1][2])+ '\n'
                       #+'Score: '+ str(jokes_list[i][1][1])+ '\n'+ '\n'+ '\n'
                       )
    return jokes_dict
