import collections
import pandas
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

df = pandas.read_csv("../../Data/merged_on_IPF.csv", na_filter='')
texts = list(df['Outcome'])

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
    trans = km_model.transform(tfidf_model)
    centres = km_model.cluster_centers_
    labels = km_model.labels_

    clustering = collections.defaultdict(list)

    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    return clustering, centres, trans, labels

clusters, centres, coordinates, lables= cluster_texts(texts, clusters=2)
colours = ['red', 'blue', 'green', 'yellow', 'orange', 'pink', 'purple']

for i in range(len(lables)):
    plt.scatter(coordinates[i][0], coordinates[i][1], color=colours[lables[i]])

plt.show()
