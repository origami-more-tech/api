from loader import scheduler, bot
import re
import csv
import pandas as pd
from aiogram import types
from pymorphy2 import MorphAnalyzer
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from random import randint
from aiogram.utils.keyboard import InlineKeyboardBuilder

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
morph = MorphAnalyzer()

recommendations = 5


def lemmatize(doc):
    doc = re.sub(patterns, " ", doc)
    tokens = []
    for token in doc.split():
        token = token.strip()
        token = morph.normal_forms(token)[0]

        tokens.append(token)
    if len(tokens) > 2:
        return " ".join(tokens)
    return None


def recomendate(search_word):
    df = pd.read_csv(
        "score.csv",
        quotechar='"',
        delimiter=",",
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True,
    )
    csr_data = csr_matrix(df.values)

    knn = NearestNeighbors(
        metric="cosine", algorithm="brute", n_neighbors=10, n_jobs=-1
    )

    # обучим модель
    knn.fit(csr_data)

    articles = pd.read_csv("articles.csv")
    articles["title"] = articles["title"].apply(lambda title: title.lower())

    articles["lemmatized"] = articles["title"].apply(lemmatize)
    article_search = articles[articles["lemmatized"].str.contains(search_word)]

    article_id = article_search.iloc[0]["article_id"]

    article_id = df[df["article_id"] == article_id].index[0]
    distances, indices = knn.kneighbors(
        csr_data[article_id], n_neighbors=recommendations + 1  # type: ignore
    )

    indices_list = indices.squeeze().tolist()
    distances_list = distances.squeeze().tolist()

    indices_distances = list(zip(indices_list, distances_list))

    indices_distances_sorted = sorted(
        indices_distances, key=lambda x: x[1], reverse=False
    )

    indices_distances_sorted = indices_distances_sorted[1:]

    recom_list = []

    for ind_dist in indices_distances_sorted:
        search_word_article_id = df.iloc[ind_dist[0]]["article_id"]

        id = articles[articles["article_id"] == search_word_article_id].index

        title = articles.iloc[id]["title"].values[0]
        url = articles.iloc[id]["url"].values[0]
        short_description = articles.iloc[id]["short_description"].values[0]
        reading_time = articles.iloc[id]["reading_time"].values[0]

        recom_list.append(
            {
                "title": title.capitalize(),
                "url": url,
                "short_description": short_description,
                "reading_time": reading_time,
            }
        )

    return recom_list


def is_job_running(job_id: str) -> bool:
    return job_id in [job.id for job in scheduler.get_jobs()]


async def ping(chat_id: str, search_word: str):
    recommended = recomendate(search_word)
    article = recommended[randint(0, len(recommended) - 1)]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Читать полностью", url=article["url"]))
    await bot.send_message(chat_id=chat_id, text="🔹")
    await bot.send_message(
        chat_id=chat_id,
        text=f"""
<b>{article["title"]}</b>

{article["short_description"]}

<i>Время прочтения ~ {int(article["reading_time"])} мин</i>
""",
        reply_markup=builder.as_markup(),
    )
