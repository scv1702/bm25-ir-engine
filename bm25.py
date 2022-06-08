from math import log
from numpy import linalg as LA

def preprocess(doc, okt):
    return okt.morphs(doc, norm=True, stem=True)

def tf(term, doc):
    return doc.count(term)

def df(term, corpus):
    df = 0
    for doc in corpus:
        if term in doc:
            df += 1
    return df

def idf(term, corpus):
    doc_freq = df(term, corpus)
    return log(len(corpus) - doc_freq + 0.5) - log(doc_freq + 0.5)

def cal_tf_idf(terms, corpus, epsilon=0.25):
    tf_list = [0] * len(terms)
    idf_list = [0] * len(terms)
    negative_idfs = list()
    idf_sum = 0

    for termId in range(len(terms)):
        # calculate tf
        temp = list()
        for doc in corpus:
            temp.append(tf(terms[termId], doc))
        tf_list[termId] = temp

        # caclulate idf
        inverse_doc_freq = idf(terms[termId], corpus)
        idf_sum += inverse_doc_freq
        idf_list[termId] = inverse_doc_freq
        if inverse_doc_freq < 0:
            negative_idfs.append(termId)

    average_idf = idf_sum / len(terms)
    eps = epsilon * average_idf

    for termId in negative_idfs:
        idf_list[termId] = eps

    return (tf_list, idf_list)

def bm25_scores(query, corpus, terms, tf_list, idf_list):
    scores = [0] * 101
    avgdl = 0
    for doc in corpus:
        avgdl += len(doc)
    avgdl = avgdl / len(corpus)
    for docId in range(len(corpus)):
        scores[docId] = bm25(query, corpus, docId, terms, tf_list, idf_list, avgdl)
    return scores

def bm25(query, corpus, docId, terms, tf_list, idf_list, avgdl, k1=1.5, b=0.75):
    score = 0
    doc_len = len(corpus[docId])
    for query_term in query:
        try:
            termId = terms.index(query_term)
            score += idf_list[termId] * (tf_list[termId][docId] * (k1 + 1)) / (tf_list[termId][docId] + k1 * (1 - b + b * doc_len / avgdl))
        except ValueError:
            continue
    return score