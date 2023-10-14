import re
import pandas as pd
from pymorphy2 import MorphAnalyzer
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
morph = MorphAnalyzer()

recommendations = 5

def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        token = token.strip()
        token = morph.normal_forms(token)[0]
        
        tokens.append(token)
    if len(tokens) > 2:
        return ' '.join(tokens)
    return None

def recomendate(search_word):
    df = pd.read_csv('score.csv')
    csr_data = csr_matrix(df.values)

    knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute', n_neighbors = 10, n_jobs = -1)
    
    # обучим модель
    knn.fit(csr_data)

    articles = pd.read_csv('articles.csv')
    articles['title'] = articles['title'].apply(lambda title: title.lower())

    articles['lemmatized'] = articles['title'].apply(lemmatize)
    article_search = articles[articles['lemmatized'].str.contains(search_word)]

    article_id = article_search.iloc[0]['article_id']
    
    article_id = df[df['article_id'] == article_id].index[0]
    distances, indices = knn.kneighbors(csr_data[article_id], n_neighbors = recommendations + 1)

    indices_list = indices.squeeze().tolist()
    distances_list = distances.squeeze().tolist()

    indices_distances = list(zip(indices_list, distances_list))

    indices_distances_sorted = sorted(indices_distances, key = lambda x: x[1], reverse = False)

    indices_distances_sorted = indices_distances_sorted[1:]

    recom_list = []

    for ind_dist in indices_distances_sorted:

        search_word_article_id = df.iloc[ind_dist[0]]['article_id']
    
        id = articles[articles['article_id'] == search_word_article_id].index
    
        title = articles.iloc[id]['title'].values[0]
        url = articles.iloc[id]['url'].values[0]
    
        recom_list.append({'title' : title.capitalize(), 'url': url})

    return recom_list