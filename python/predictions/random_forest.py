import logging
import pandas as pd
import sklearn
from sklearn.datasets import make_blobs
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from settings import Config

def simple_test():

    # simple test
    X, y = make_blobs(n_samples=10000, n_features=10, centers=100, random_state=0)
    clf = DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
    scores = cross_val_score(clf, X, y)
    logging.info(scores.mean())

    clf = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    scores = cross_val_score(clf, X, y)
    logging.info(scores.mean())

    clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    scores = cross_val_score(clf, X, y)
    logging.info(scores.mean() > 0.999)

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info(sklearn.__version__)

    # read the datatype matrix
    df = pd.read_csv(Config.VERSION2_SCORE_FILES['output_datatype_scores'])
    



if __name__ == "__main__":
    main()