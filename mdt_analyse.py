from nltk.tokenize import word_tokenize
import pandas, random, nltk

df = pandas.read_table("../../Data/merged3.csv", sep=",")

all_words = []
for i in df['Outcome'][:-1]:
    for j in word_tokenize(str(i).lower()):
        all_words.append(j)

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())


def find_features(document):
    words = set(document)
    features = {w: w in words for w in word_features}
    return features


documents = []
for i in range(len(df['Outcome'])):
    documents.append((word_tokenize(str(df['Outcome'][i]).lower()), str(df['Deceased'][i])))

random.shuffle(documents)

feature_sets = [(find_features(rev), category) for (rev, category) in documents]

training_set = feature_sets[:849]
testing_set = feature_sets[849:]
nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("NB Accuracy =", (nltk.classify.accuracy(nb_classifier, testing_set)) * 100, "%")
nb_classifier.show_most_informative_features(20)
