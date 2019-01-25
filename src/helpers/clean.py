from nltk.corpus import stopwords
import re
stopwords = set(stopwords.words('english'))

# filter out token
def valid_tkn(tkn):
    # stopwords
    if tkn in stopwords:
        return False

    # ampersand and twitter link
    twitter_stop = ['&amp;', '//t.co/', 'rt', 'http']
    if any(substr in tkn for substr in twitter_stop):
        return False

    # special unicode character
    if any(ord(c) > 128 for c in tkn):
        return False

    regex = re.compile('[^a-zA-Z]')
    tkn = regex.sub('', tkn)
    if len(tkn) < 2:
        return False
    return True

