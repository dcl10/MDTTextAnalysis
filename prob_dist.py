from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, names, words
import pandas, random, nltk, matplotlib.pyplot as pt, numpy as np, string

df = pandas.read_table("../../Data/merged_on_Sarcoid.csv", sep=",")

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

# Extract all words that are not stop words or basic English
all_words = []
for i in df['Outcome'][:-1]:
    for j in word_tokenize(str(i).lower()):
        if j not in name_list and j not in sw and j not in basic_words:
            all_words.append(j)

# Not sure why this is here, I was just following the tutorial
all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())

# Find if a word is in the document and store a dict where the key is the word and the value is True or False
# depending on if the word is in the document
def find_features(document):
    words = set(document)
    features = {w: w in words for w in word_features}
    return features

# Retrieve the MDT outcomes and describe if it is in a patient with or without the condition
documents = []
for i in range(len(df['Outcome'])):
    documents.append((word_tokenize(str(df['Outcome'][i]).lower()), str(df['Sarcoid'][i])))

# Shuffle the documents before setting up the machine learning algorithm
random.shuffle(documents)

# Define the feature sets and then divide them into the training and testing sets
feature_sets = [(find_features(rev), category) for (rev, category) in documents]
training_set = feature_sets[:int(len(feature_sets)*0.8)]
testing_set = feature_sets[int(len(feature_sets)*0.8):]

nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
prob_dist_false = []
prob_dist_true = []
for i in range(0, len(testing_set[:-1])):
    if nb_classifier.classify(testing_set[i][0]) == str(0):
        prob_dist_false.append(nb_classifier.prob_classify(testing_set[i][0]).logprob(testing_set[i][1]))
    elif nb_classifier.classify(testing_set[i][0]) == str(1):
        prob_dist_true.append(nb_classifier.prob_classify(testing_set[i][0]).logprob(testing_set[i][1]))

# Method to separate the significant
def get_sig_hits(log_prob_dists):
    sig_list = []
    non_sig_list = []
    for i in log_prob_dists:
        if i >= -0.07: sig_list.append(i)
        else: non_sig_list.append(i)
    return sig_list, non_sig_list

sig_false, non_sig_false = get_sig_hits(prob_dist_false)
sig_true, non_sig_true = get_sig_hits(prob_dist_true)

# Create bar chart to compare the number of significant hits
objects = ('Sig True', 'Non-sig True', 'Sig False', 'Non-sig False')
y_pos = np.arange(len(objects))
pt.bar(y_pos, [len(sig_true), len(non_sig_true), len(sig_false), len(non_sig_false)])
pt.xticks(y_pos, objects)
pt.title("Comparison of performance of Naive Bayes algorithm")
pt.xlabel("Category")
pt.ylabel("Number of Patients")
#pt.savefig("../../Data/Plots/Sarcoid_bar.jpg")
pt.show()
pt.clf()

for i in range(len(prob_dist_false)):
    if prob_dist_false[i] >= -0.07: pt.scatter(i, prob_dist_false[i], color='blue')
    else: pt.scatter(i, prob_dist_false[i], color='red')

pt.ylabel("Log 2 Probability")
pt.xlabel("Patient")
pt.title("Log 2 Probability of correctly predicting not having Sarcoid")
#pt.savefig("../../Data/Plots/nonSarcoid.jpg")
pt.show()
pt.clf()

for i in range(len(prob_dist_true)):
    if prob_dist_true[i] >= -0.07: pt.scatter(i, prob_dist_true[i], color='blue')
    else: pt.scatter(i, prob_dist_true[i], color='red')

pt.ylabel("Log 2 Probability")
pt.xlabel("Patient")
pt.title("Log 2 Probability of correctly predicting having Sarcoid")
#pt.savefig("../../Data/Plots/Sarcoid.jpg")
pt.show()
