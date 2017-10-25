from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, names, words
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

import pandas, random, nltk, string


df = pandas.read_table("../../Data/merged_on_Emphysema.csv", sep=",")

# Refinement by removal of junk words
sw = list(stopwords.words('english'))
sw.extend(list(string.punctuation))
name_list = list(names.words('male.txt'))
name_list.extend(list(names.words('female.txt'))+['goodman', 'mr', 'mrs', 'dr', 'miss'])
# Names are capitalised, so not recognised when trying to remove them. Thus make them all lowercase
for i in range(len(name_list)):
     name_list[i] = str(name_list[i]).lower()
# To remove over simple English words
basic_words = list(words.words('en-basic'))

all_words = []
for i in df['Outcome'][:-1]:
    for j in word_tokenize(str(i).lower()):
        if j not in name_list and j not in sw and j not in basic_words:
            all_words.append(j)

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())


def find_features(document):
    words = set(document)
    features = {w: w in words for w in word_features}
    return features


documents = []
for i in range(len(df['Outcome'])):
    documents.append((word_tokenize(str(df['Outcome'][i]).lower()), str(df['Emphysema'][i])))

nb_accuracy = []
bnb_accuracy = []
mnb_accuracy = []
svc_accuracy = []
knn_accuracy = []
for i in range(100):
    random.shuffle(documents)

    feature_sets = [(find_features(rev), category) for (rev, category) in documents]

    training_set = feature_sets[:int(len(feature_sets)*0.5)]
    testing_set = feature_sets[int(len(feature_sets)*0.5):]


    nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
    #print("nltk NB Accuracy =", (nltk.classify.accuracy(nb_classifier, testing_set)) * 100)
    nb_accuracy.append((nltk.classify.accuracy(nb_classifier, testing_set)) * 100)

    bnb_classifier = SklearnClassifier(BernoulliNB()).train(training_set)
    #print("sklearn Bernoulli NB accuracy =", (nltk.classify.accuracy(bnb_classifier, testing_set)) * 100)
    bnb_accuracy.append((nltk.classify.accuracy(bnb_classifier, testing_set)) * 100)

    mnb_classifier = SklearnClassifier(MultinomialNB()).train(training_set)
    #print("sklearn Multinomial NB accuracy =", (nltk.classify.accuracy(mnb_classifier, testing_set)) * 100)
    mnb_accuracy.append((nltk.classify.accuracy(mnb_classifier, testing_set)) * 100)

    svc_classifier = SklearnClassifier(SVC()).train(training_set)
    #print("sklearn SVC accuracy =", (nltk.classify.accuracy(svc_classifier, testing_set)) * 100)
    svc_accuracy.append((nltk.classify.accuracy(svc_classifier, testing_set)) * 100)

    knn_classifier = SklearnClassifier(KNeighborsClassifier()).train(training_set)
    #print("sklearn K-Neighbours accuracy =", (nltk.classify.accuracy(knn_classifier, testing_set)) * 100)
    knn_accuracy.append((nltk.classify.accuracy(knn_classifier, testing_set)) * 100)

print("Average NB = ", sum(nb_accuracy)/len(nb_accuracy))
print("Average BNB = ", sum(bnb_accuracy)/len(bnb_accuracy))
print("Average MNB = ", sum(mnb_accuracy)/len(mnb_accuracy))
print("Average SVC = ", sum(svc_accuracy)/len(svc_accuracy))
print("Average KNN = ", sum(knn_accuracy)/len(knn_accuracy))
