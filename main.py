from rank_bm25 import BM25Okapi
from konlpy.tag import Hannanum

hannanum = Hannanum()
contents = list()
tokenized_contents = list()
titles = list()

# preprocess corpus
with open("corpus.txt", "r") as f:
    line = f.readline()
    while line:
        # preprocess title
        title = line.replace("<title>","").replace("</title>","").replace("\n","")
        title = title[title.find(".")+2:]
        titles.append(title)
        
        # preprocess content
        content = f.readline()
        tokenized_content = hannanum.morphs(content)

        # save the preprocessed document to corpus
        contents.append(content)
        tokenized_contents.append(tokenized_content)

        # read space
        _ = f.readline()

        # read next title
        line = f.readline()

# tokenize corpus
bm25 = BM25Okapi(tokenized_contents)

# get query
print("Query: ", end="")
query = input()

# tokenize query
tokenized_query = hannanum.morphs(query)

# caclulate tf-idf scores between query and corpus
doc_scores = bm25.get_scores(tokenized_query)

# get top 5 documents
top_5_doc_ids = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i])[-5:]
top_5_doc_ids.reverse()

# print top 5 documents
for doc_id in top_5_doc_ids:
    print(f"DocId: {doc_id + 1} Score: {doc_scores[doc_id]}")
    print(titles[doc_id])
    print(contents[doc_id])