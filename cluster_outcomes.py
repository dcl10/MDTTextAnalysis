import collections, pandas, matplotlib.pyplot as plt, nltk

from nltk.corpus import stopwords, names, words
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

df = pandas.read_csv("../../Data/merged_on_Emphysema.csv", na_filter='')
texts = list(df['Outcome'])

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
def remove_junk(text):
    all_words = []
    for j in word_tokenize(text.lower()):
        if j not in name_list and j not in sw and j not in basic_words:
            all_words.append(j)
    # convert to sentence
    doc = "".join(word + " " for word in all_words)
    return doc

# Remove junk words from the documents
texts = list(remove_junk(str(i)) for i in texts)

# robbed from: "http://nlpforhackers.io/recipe-text-clustering/"
def cluster_texts(texts, clusters=3):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(tokenizer=word_tokenize,
                                 stop_words=stopwords.words('english'),
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)

    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)

    # the following two lines are my adaptation
    # trans is the cluster-distance space for the dataset to be plotted
    # labels are the clusters each document belongs to
    trans = km_model.transform(tfidf_model)
    labels = km_model.labels_

    clustering = collections.defaultdict(list)

    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    # modified to return centres, trans and labels
    return clustering, trans, labels

clusters, coordinates, labels = cluster_texts(texts, clusters=2)
colours = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'purple']

for i in range(len(labels)):
    plt.scatter(coordinates[i][0], coordinates[i][1], color=colours[labels[i]])

plt.title("Plot of cluster-distance matrix from k means clustering")
plt.show()

cluster_0_docs = [texts[i] for i in clusters[0]]
cluster_1_docs = [texts[i] for i in clusters[1]]
print(cluster_0_docs)
print(cluster_1_docs)
words_0 = []
for i in cluster_0_docs:
    words_0.extend(word_tokenize(i))

print(words_0)