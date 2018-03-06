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

def random_forest_classifier(features, target):
    """
    To train the random forest classifier with features and target data
    :param features:
    :param target:
    :return: trained random forest classifier
    """
    clf = RandomForestClassifier()
    clf.fit(features, target)
    return clf

def split_dataset(dataset, train_percentage, feature_headers, target_header):
    """
    Split the dataset with train_percentage
    :param dataset:
    :param train_percentage:
    :param feature_headers:
    :param target_header:
    :return: train_x, test_x, train_y, test_y
    """

    # Split dataset into train and test dataset
    train_x, test_x, train_y, test_y = train_test_split(dataset[feature_headers], dataset[target_header],
                                                        train_size=train_percentage)
    return train_x, test_x, train_y, test_y

def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info(sklearn.__version__)

    # read the datatype matrix
    df = pd.read_csv(Config.VERSION2_SCORE_FILES['gene_disease_associations_datatypes'], index_col=0)

    d = {'True': True, 'False': False}
    print(df['is_direct'].dtype)

    # look at the daa (statistics)
    #print df.describe()

    # get the data where is_direct is true and where there is some DRUG information
    cond1 = (df['known_drug'] > 0.0) & (df['is_direct'])
    df_chembl = df[cond1]
    df_chembl['key'] = df_chembl.ensembl_gene_id.astype(str).str.cat(df_chembl.disease_id.astype(str), sep='-')
    df_chembl = df_chembl.assign(y=df['known_drug'].apply(lambda x: int(x*10)))
    print(df_chembl['key'])
    # remove 'overall_score' for the time being
    df_chembl_pred = df_chembl[['key',  'genetic_association', 'somatic_mutation', 'rna_expression', 'affected_pathway', 'animal_model', 'literature', 'y']]

    # get headers
    headers = list(df_chembl_pred.columns.values)
    print(headers)
    print(headers[1:-1])
    print(headers[-1])

    # Split the data in train and tests
    train_x, test_x, train_y, test_y = split_dataset(df_chembl_pred, 0.7, headers[1:-1], headers[-1])

    # Train and Test dataset size details
    '''
    print "Train_x Shape :: ", train_x.shape
    print "Train_y Shape :: ", train_y.shape
    print "Test_x Shape :: ", test_x.shape
    print "Test_y Shape :: ", test_y.shape
    '''

    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print "Trained model :: ", trained_model

    predictions = trained_model.predict(test_x)

    for i in xrange(0, 5):
        print "Actual outcome :: {} and Predicted outcome :: {}".format(list(test_y)[i], predictions[i])

    print "Train Accuracy :: ", accuracy_score(train_y, trained_model.predict(train_x))
    print "Test Accuracy  :: ", accuracy_score(test_y, predictions)
    print " Confusion matrix ", confusion_matrix(test_y, predictions)



if __name__ == "__main__":
    main()