import csv
import math
import numpy as np
from numpy.linalg import norm

from gensim import corpora, models, matutils
from pprint import pprint

def unions(l1, l2):
    return list(set().union(l1, l2))


def parse(filename):

    with open(filename, 'r') as f:
        data = csv.reader(f)
        data = list(data)

    return data


dup = parse('parsed_dup.csv')
dup = dup[1:]                                       # Removing headers

pastq = parse('parsed_SU.csv')
pastq = pastq[1:]


titles_data = []
desc_data = []

# getting all past q titles and decs
for p in pastq:

    # title
    p_0 = p[0].replace("'", "").strip('][').split(', ')     #changing from string to list

    titles_data = unions(titles_data, p_0)

    # description
    p_2 = p[2].replace("'", "").strip('][').split(', ')

    desc_data = unions(desc_data, p_2)


# topic data
u_topic = unions(titles_data, desc_data)

#building LDA model on past q
dataset = [d.split() for d in u_topic]
id2word_dict = corpora.Dictionary(dataset)       #maps each word to a unique id

corpus = [id2word_dict.doc2bow(word) for word in dataset]        #maps word ids to word frequencies

# number of topics (this should be 100 according to the paper)
num_topics = 12

# Build LDA model
lda_model = models.LdaMulticore(corpus=corpus, id2word=id2word_dict, num_topics=num_topics, minimum_probability=0.0)

# # Print the Keywords in the 10 topics and the keywords contributions to the topic
# pprint(lda_model.print_topics())
# doc_lda = lda_model[corpus]


title_score=[]
tag_score=[]
desc_score=[]
topic_score=[]

for i in dup:
    for j in pastq:

        # title
        title_i = []
        title_j = []

        i_0 = i[0].replace("'", "").strip('][').split(', ')     #changing from string to list
        j_0 = j[0].replace("'", "").strip('][').split(', ')

        u_title = unions(i_0, j_0)
        size_i = 0
        size_j = 0

        for idx, word in enumerate(u_title):
            title_i.append(i_0.count(word)/len(i_0))      # Normalizing to wt
            title_j.append(j_0.count(word)/len(j_0))
            size_i += (i_0.count(word)/len(i_0))**2
            size_j += (j_0.count(word)/len(j_0))**2     # Size parameter for denominator

        title_score.append( np.dot(title_i, title_j) / (math.sqrt(size_i)*math.sqrt(size_j)) )

        print("title: ")
        print(np.dot(title_i, title_j)/ (math.sqrt(size_i)*math.sqrt(size_j)))


        # tags
        tag_i = []
        tag_j = []

        i_1 = i[1].replace("'", "").strip('][').split(', ')
        j_1 = j[1].replace("'", "").strip('][').split(', ')

        u_tag = unions(i_1, j_1)
        size_i = 0
        size_j = 0

        for idx, word in enumerate(u_tag):
            tag_i.append(i_1.count(word)/len(i_1))      # Normalizing to wt
            tag_j.append(j_1.count(word)/len(j_1))
            size_i += (i_1.count(word)/len(i_1))**2
            size_j += (j_1.count(word)/len(j_1))**2     # Size parameter for denominator

        tag_score.append( np.dot(tag_i, tag_j) / (math.sqrt(size_i)*math.sqrt(size_j)) )

        print("tag: ")
        print( np.dot(tag_i, tag_j) / (math.sqrt(size_i)*math.sqrt(size_j)) )


        # description
        desc_i = []
        desc_j = []

        i_2 = i[2].replace("'", "").strip('][').split(', ')
        j_2 = j[2].replace("'", "").strip('][').split(', ')

        u_desc = unions(i_2, j_2)
        size_i = 0
        size_j = 0

        for idx, word in enumerate(u_desc):
            desc_i.append(i_2.count(word)/len(i_2))      # Normalizing to wt
            desc_j.append(j_2.count(word)/len(j_2))
            size_i += (i_2.count(word)/len(i_2))**2
            size_j += (j_2.count(word)/len(j_2))**2     # Size parameter for denominator

        desc_score.append( np.dot(desc_i, desc_j) / (math.sqrt(size_i)*math.sqrt(size_j)) )

        print("desc: ")
        print( np.dot(desc_i, desc_j) / (math.sqrt(size_i)*math.sqrt(size_j)) )


        # topic
        i_topics = unions(i_0, i_2)
        corpus_i = id2word_dict.doc2bow(i_topics)
        prob_i = np.array(lda_model[corpus_i])[:,1] 
        doc_i = lda_model[corpus_i]

        j_topics = unions(j_0, j_2)
        corpus_j = id2word_dict.doc2bow(j_topics)
        prob_j = np.array(lda_model[corpus_j])[:,1] 
        doc_j = lda_model[corpus_j]

        topic_score.append( np.dot(prob_i, prob_j) / ( norm(prob_i)*norm(prob_j) ) )
        #topic_score.append( matutils.cossim(doc_i, doc_j) )
        
        print("topic: ")
        # print( lda_model.get_document_topics(corpus_i) )
        # print( lda_model.get_document_topics(corpus_j) )

        #print(matutils.cossim(doc_i, doc_j))
        print( np.dot(prob_i, prob_j) / ( norm(prob_i)*norm(prob_j) ) )
        print()
        

# print(title_score)
# print(tag_score)
# print(desc_score)
# print(topic_score)

print(len(dup))
print(len(pastq))


title_score = np.array(title_score)
tag_score = np.array(tag_score)
desc_score = np.array(desc_score)
topic_score = np.array(topic_score)

np.reshape(title_score, (len(dup), len(pastq)))
np.reshape(tag_score, (len(dup), len(pastq)))
np.reshape(desc_score, (len(dup), len(pastq)))
np.reshape(topic_score, (len(dup), len(pastq)))
