"""
Downloads and creates topics from your mail. Model will be saved to ../data/pickles/
If path doesn't exist script will create one.

You need to fill configure.py with your credits:
    FROM_EMAIL  -- your mail address (example@elpmaxe.com)
    FROM_PWD    -- password from your mail address
    SMPT_SERVER -- mail server. For gmail fill 'imap.gmail.com'
    SMPT_PORT   -- 993 (duno)
"""


import src.configure as config
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from src.MailCrawler import MailCrawler
from time import time
from os.path import exists
from os import makedirs
from utils import print_top_words

if __name__ == '__main__':

    save_path = '../data/pickles/'
    n_topics = 10

    print('-'*100)
    print('Loading stopwords..')
    print('-'*100)

    with open('../data/stop_words.txt') as sw:
        stop_words = [s.strip() for s in sw]
    print('Connecting to mail server')
    mc = MailCrawler(config.SMPT_SERVER, config.FROM_EMAIL,
                     config.FROM_PWD, config.SMPT_PORT)
    mc.connect()
    print('Connected!')
    print('-'*100)

    clf = LatentDirichletAllocation(n_topics)
    count_vect = CountVectorizer(stop_words=stop_words)

    print('Fitting count_vectorizer')
    mat = count_vect.fit_transform(mc.get_text())
    print('Done!')
    print('-'*100)

    print('Fitting LDA model')
    clf.fit(mat)
    print('Done!')
    print('-'*100)

    print('Perplexity = {}'.format(clf.perplexity(mat)))
    print('-'*100)

    print('Topics:')
    print_top_words(clf, count_vect.get_feature_names(), 10)
    print('-'*100)

    mc.disconnect()

    print('Saving to ' + save_path)
    if not exists(save_path):
        print('Path doesn\'t exist, creating one')
        makedirs(save_path)
    with open(save_path + 'lda_model_' + str(int(time())) + '.pickle', 'wb') as f:
        pickle.dump(clf, f)
    print('-'*100)
