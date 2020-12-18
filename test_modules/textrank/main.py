from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk import sent_tokenize, word_tokenize
from operator import itemgetter
import numpy as np

# Get Contents ##
text = ""
f = open("D:\\BE_Project_v1\\test_modules\\textrank\\MemoryManagement.txt", "r")
# f = open("D:\\BE_Project_v1\\test_modules\\textrank\\ProcessManagement.txt", "r")
# f = open("D:\\BE_Project_v1\\test_modules\\textrank\\Deadlock.txt", "r")
for x in f.readlines():
    text += x
f.close()

# Tokenize the sentences and remove punctuations  ##
sent_text = sent_tokenize(text)

result_sentences = []
for sentence in sent_text:
    tokenized_text = word_tokenize(sentence)
    new_words= [word for word in tokenized_text if word.isalnum()]
    result_sentences.append(new_words)

# for x in result_sentences:
#     print(x)


# Text Rank Implementation ##
def textrank(sentences, top_n=5, stopwords=None):
    S = build_similarity_matrix(sentences, stop_words)
    sentence_ranks = pagerank(S)

    # Sort the sentence ranks
    ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    summary = itemgetter(*selected_sentences)(sentences)
    return summary


def build_similarity_matrix(sentences, stopwords=None):
    # Create an empty similarity matrix
    S = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue

            S[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    # normalize the matrix row-wise
    for idx in range(len(S)):
        if S[idx].sum()==0:
            continue
        S[idx] /= S[idx].sum()

    return S


def pagerank(A, eps=0.0001, d=0.85):
    P = np.ones(len(A)) / len(A)
    while True:
        new_P = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P


def sentence_similarity(sent1, sent2, stopwords=None):

    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)


stop_words = stopwords.words('english')

for x in textrank(result_sentences, 6, stop_words):
    print(x)



# output
# ['It', 'also', 'protects', 'the', 'resources', 'of', 'each', 'process', 'from', 'other', 'methods', 'and', 'allows', 'synchronization', 'among', 'processes']
# ['The', 'information', 'is', 'quickly', 'updated', 'in', 'the', 'PCB', 'by', 'the', 'OS', 'as', 'soon', 'as', 'the', 'process', 'makes', 'the', 'state', 'transition']
# ['A', 'process', 'state', 'is', 'a', 'condition', 'of', 'the', 'process', 'at', 'a', 'specific', 'instant', 'of', 'time']
# ['It', 'also', 'defines', 'the', 'current', 'position', 'of', 'the', 'process']
# ['Executing', 'The', 'process', 'is', 'an', 'execution', 'state']
# ['Suspended', 'Suspended', 'state', 'defines', 'the', 'time', 'when', 'a', 'process', 'is', 'ready', 'for', 'execution', 'but', 'has', 'not', 'been', 'placed', 'in', 'the', 'ready', 'queue', 'by', 'OS']



# original
# ['Process', 'management', 'involves', 'various', 'tasks', 'like', 'creation', 'scheduling', 'termination', 'of', 'processes', 'and', 'a', 'deadlock']
# ['Process', 'is', 'a', 'program', 'that', 'is', 'under', 'execution', 'which', 'is', 'an', 'important', 'part', 'of', 'operating', 'systems']
# ['The', 'OS', 'must', 'allocate', 'resources', 'that', 'enable', 'processes', 'to', 'share', 'and', 'exchange', 'information']
# ['It', 'also', 'protects', 'the', 'resources', 'of', 'each', 'process', 'from', 'other', 'methods', 'and', 'allows', 'synchronization', 'among', 'processes']
# ['It', 'is', 'the', 'job', 'of', 'OS', 'to', 'manage', 'all', 'the', 'running', 'processes', 'of', 'the', 'system']
# ['It', 'handles', 'operations', 'by', 'performing', 'tasks', 'like', 'process', 'scheduling', 'and', 'such', 'as', 'resource', 'allocation']
# ['The', 'PCB', 'is', 'a', 'full', 'form', 'of', 'Process', 'Control', 'Block']
# ['It', 'is', 'a', 'data', 'structure', 'that', 'is', 'maintained', 'by', 'the', 'Operating', 'System', 'for', 'every', 'process']
# ['The', 'PCB', 'should', 'be', 'identified', 'by', 'an', 'integer', 'Process', 'ID', 'PID']
# ['It', 'helps', 'you', 'to', 'store', 'all', 'the', 'information', 'required', 'to', 'keep', 'track', 'of', 'all', 'the', 'running', 'processes']
# ['It', 'is', 'also', 'accountable', 'for', 'storing', 'the', 'contents', 'of', 'processor', 'registers']
# ['These', 'are', 'saved', 'when', 'the', 'process', 'moves', 'from', 'the', 'running', 'state', 'and', 'then', 'returns', 'back', 'to', 'it']
# ['The', 'information', 'is', 'quickly', 'updated', 'in', 'the', 'PCB', 'by', 'the', 'OS', 'as', 'soon', 'as', 'the', 'process', 'makes', 'the', 'state', 'transition']
# ['A', 'process', 'state', 'is', 'a', 'condition', 'of', 'the', 'process', 'at', 'a', 'specific', 'instant', 'of', 'time']
# ['It', 'also', 'defines', 'the', 'current', 'position', 'of', 'the', 'process']
# ['There', 'are', 'mainly', 'seven', 'stages', 'of', 'a', 'process', 'which', 'are', 'New', 'The', 'new', 'process', 'is', 'created', 'when', 'a', 'specific', 'program', 'calls', 'from', 'secondary', 'hard', 'disk', 'to', 'primary', 'RAM']
# ['Ready', 'In', 'a', 'ready', 'state', 'the', 'process', 'should', 'be', 'loaded', 'into', 'the', 'primary', 'memory', 'which', 'is', 'ready', 'for', 'execution']
# ['Waiting', 'The', 'process', 'is', 'waiting', 'for', 'the', 'allocation', 'of', 'CPU', 'time', 'and', 'other', 'resources', 'for', 'execution']
# ['Executing', 'The', 'process', 'is', 'an', 'execution', 'state']
# ['Blocked', 'It', 'is', 'a', 'time', 'interval', 'when', 'a', 'process', 'is', 'waiting', 'for', 'an', 'event', 'like', 'operations', 'to', 'complete']
# ['Suspended', 'Suspended', 'state', 'defines', 'the', 'time', 'when', 'a', 'process', 'is', 'ready', 'for', 'execution', 'but', 'has', 'not', 'been', 'placed', 'in', 'the', 'ready', 'queue', 'by', 'OS']
# ['Terminated', 'Terminated', 'state', 'specifies', 'the', 'time', 'when', 'a', 'process', 'is', 'terminated']
# ['After', 'completing', 'every', 'step', 'all', 'the', 'resources', 'are', 'used', 'by', 'a', 'process', 'and', 'memory', 'becomes', 'free']
