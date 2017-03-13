from .MailCategorizator import Preprocessor
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

import pickle
if __name__ == '__main__':
    preprocessor = Preprocessor()
    binarizer = MultiLabelBinarizer()
    clf = MultiOutputClassifier(RandomForestClassifier(), n_jobs=-1)

    X = preprocessor.build_tfidf_matrix()
    y = binarizer.fit_transform(preprocessor.get_target())

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    clf.fit(x_train, y_train)
    print(clf.score(x_test, y_test))

    pickle.dump(clf, '../data/pickles/')
    pickle.dump(preprocessor, '../data/pickles/')