from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, names, words
import pandas, random, nltk, matplotlib.pyplot as pt

df = pandas.read_table("../../Data/merged_on_IPF.csv", sep=",")

# Refinement by removal of junk words
sw = list(stopwords.words('english'))
sw.extend(["?", "<", ">", ",", ".", '+', '-', '(', ')', '%'])
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
    documents.append((word_tokenize(str(df['Outcome'][i]).lower()), str(df['IPF'][i])))

# Shuffle the documents before setting up the machine learning algorithm
random.shuffle(documents)

# Define the feature sets and then divide them into the training and testing sets
feature_sets = [(find_features(rev), category) for (rev, category) in documents]
training_set = feature_sets[:int(len(feature_sets)*0.5)]
testing_set = feature_sets[int(len(feature_sets)*0.5):]

nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
prob_dist_false = []
prob_dist_true = []
for i in range(0, len(testing_set[:-1])):
    #print(nb_classifier.prob_classify(testing_set[i][0]).prob(testing_set[i][1]))
    if testing_set[i][1] == str(0):
        prob_dist_false.append(nb_classifier.prob_classify(testing_set[i][0]).logprob(testing_set[i][1]))
    elif testing_set[i][1] == str(1):
        prob_dist_true.append(nb_classifier.prob_classify(testing_set[i][0]).logprob(testing_set[i][1]))

pt.scatter(range(len(prob_dist_false)), prob_dist_false, color='red')
pt.title("Probability distribution for non-IPF")
pt.xlabel("Patient")
pt.ylabel("log e Probability")
pt.savefig("../../Data/Plots/nonIPFscatter.jpg")
pt.clf()

pt.scatter(range(len(prob_dist_true)), prob_dist_true, color='blue')
pt.title("Probability distribution for IPF")
pt.xlabel("Patient")
pt.ylabel("log e Probability")
pt.savefig("../../Data/Plots/IPFscatter.jpg")
