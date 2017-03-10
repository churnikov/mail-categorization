from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from os.path import join, isdir
from os import listdir

import json
import pickle 
import re

class Preprocessor(TfidfVectorizer):
"""
Preprocesses jsons from specified path. 
They should have structure:

{
    "Text" : "Text of mail message",
    "Title" : "Title of mail",
    "From" : ["example1@sample1.ru", "woah@haow.by"],
    "To" : ["example2@sample2.ru", "my@student.ru"],
    "Categories" : ["Work", "Cooking", "Pickle"]
}
"""
        
    def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        """
        Call in a loop to create terminal progress bar
        :params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        sys.stdout.flush()
        # Print New Line on Complete
        if iteration == total:
            sys.stdout.write('\n')


    def read_json(path):
        """
        Gets path+file_name of json file.

        returns dict representation of json
        """
        json_dict = None
        try:
            with open(path, 'r') as f:
                s = ''.join([l.strip() for l in f])
                try:
                    json_dict = json.loads(s)
                except:
                    raise FileExistsError('Problem with json {}'.format(path))
        except:
            raise FileExistsError('Problem with {}'.format(path))
        return json_dict


    def __list_files_w_type(self, typ='.json'):
    """
    Lists files with type in self.directory.
    :params:
        typ - Optional: type of files that would be looked up in directory
            - (Str)
            - default value: '.json'
    :returns:
            - (list)
            - files in self.directory
            - if directory doesn'n exist or no files found, raises FileNotFoundError
    """
        if isdir(self.directory):
            return [join(self.directory, f) for f in listdir(self.directory) if f.endswith(typ)]
        raise FileNotFoundError('Directory {} not found or no files with type {} found'.format(self.directory, typ)) 


    def __init__(self, directory='../data/', 
                labels={"Text": "Text", "Title": "Title", "From" : "From", "To": "To"}, 
                target={"Target" : "Categories"},
                **kwargs):
        """
        Initializes child of sklearn's TfidfVectorizer. Takes directory, where jsons are located. 
        :params:
            directory - Optional : directory where jsons are located
                      - (Str) 
                      - default value: ../data/
            labels    - Optional : dictionary that should have these keys: {"Text", "Title", "From", "To"}. 
                                   This dictionary describes how these objects named in your jsons. 
                      - (dict)
                      - default value: {"Text": "Text", "Title": "Title", "From" : "From", "To": "To"}
            target    - Optional : dict with one key, value pair.
                        This dictionary describes how target variable named in your jsons. 
                      - (dict)
                      - default value: {"Target" : "Categories"}.
            kwargs    - dict for values in TfidfVectorizer
                      - (dict)
        """ 
        self.vectorizer = super(Preprocessor, self).__init__(**kwargs)
        self.directory = directory
        self.labels = labels
        self.target = target     

    
