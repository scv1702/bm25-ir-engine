from konlpy.tag import Okt
from bm25 import cal_tf_idf, preprocess, bm25_scores

corpus = [0] * 100
titles = [0] * 100
contents = [0] * 100
terms = list()
okt = Okt()

with open("corpus.txt", "r") as f:
    line = f.readline()
    docId = 0
    while line:
        # preprocess title
        title = line.replace("<title>","").replace("</title>","").replace("\n","")
        title = title[title.find(".")+2:]
        # preprocess content
        content = f.readline()
        preprocessed_content = preprocess(content, okt)
        titles[docId] = title
        contents[docId] = content
        corpus[docId] = preprocessed_content
        temp = list()
        for token in preprocessed_content:
            if token not in terms:
                temp.append(token)
        terms += temp
        # read space
        _ = f.readline()
        # read next title
        line = f.readline()
        docId += 1

terms.sort()

tf_list, idf_list = cal_tf_idf(terms, corpus)

# get query
print("Query: ", end="")
query = input()

while query != "종료":
    # calculate cosine_similarity between query and documents
    preprocessed_query = preprocess(query, okt)
    scores = bm25_scores(preprocessed_query, corpus, terms, tf_list, idf_list)
    top_5_docId = sorted(range(len(scores)), key=lambda i: scores[i])[-5:]
    top_5_docId.reverse()
    # print top 5 documents
    for docId in top_5_docId:
        print(f"DocId: {docId + 1} Score: {scores[docId]}")
        print(titles[docId])
        print(contents[docId])
    # get query
    print("Query: ", end="")
    query = input()