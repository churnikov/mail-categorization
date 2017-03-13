import sys

sys.path.append('../src/')

import unittest
import json
import tempfile

from src.MailCategorizator import Preprocessor


class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.prep = Preprocessor(directory='../data/test_data/')
        self.jsn = {"Text": "Text ext", "Title": "Title", "Content": ["Content"]}

    def test___read_jsons(self):
        read_jsn = self.prep._Preprocessor__read_jsons()
        for r in read_jsn:
            print(r)
            self.assertEqual(r, self.jsn, 'Reads jsons wrong')

    def test_build_tfidf_matrix(self):
        print(self.prep.build_tfidf_matrix().shape)


if __name__ == '__main__':
    unittest.main()
