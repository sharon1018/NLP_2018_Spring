# mapper
import re, sys

def tokens(str1): return re.findall('[a-z]+', str1.lower().strip())

def ngrams(sent, n):
    return [ ' '.join(x) for x in zip(*[sent[i:] for i in range(n) if i <= len(sent) ] ) ]

def good_coll_examples():
    good_colls = set()
    for line in open('bnc.coll.small.txt','r'):
        element = line.split('\t')
        good_colls.add((element[0],element[1],int(element[2])))
    return good_colls

good_coll_examples = good_coll_examples()

def is_good_coll(base_word, coll, dist):
    if (base_word, coll, dist) in good_coll_examples:
        return True    

for line in sys.stdin:
    sent = tokens(line)
    for n in range(2, 6):
        for ngram in ngrams(sent, n):
            ngram = ngram.split(' ')
            first = ngram[0]
            last = ngram[-1]
            if is_good_coll(first, last,(n-1)):
                print('%s_%s_%s\t%s' % (first, last,str((n-1)),line.strip()))
            if is_good_coll(last, first,(1-n)):
                print('%s_%s_%s\t%s' % (last, first,str((1-n)),line.strip()))

# reducer
import re, sys
from collections import defaultdict, Counter

def tokens(str1): return re.findall('[a-z]+', str1.lower().strip())

def high_freq_words():
    word_list = set()
    for line in open('HiFreWords','r'):
        for word in line.split('\t'):
            word_list.add(word)
    return word_list
            
high_freq_list = high_freq_words()

def pron_words():
    pron_list = set()
    for pron in open('prons.txt','r'):
        pron_list.add(pron.strip())
    return pron_list

pron_list = pron_words()

def compute_score(word, sentence):
    sent = tokens(sentence)
    word_loc = sent.index(word) + 1
    not_high_freq = 0
    prons = 0
    for word in sent:
        if word not in high_freq_list: not_high_freq += 1
        if word in pron_list: prons += 1
    return (word_loc - not_high_freq - prons)

collocation_sentences = defaultdict(lambda:[])

for line in sys.stdin:
    row = line.strip().split('\t')
    collocation = tuple(row[0].split('_'))
    sentence = row[1]
    collocation_sentences[collocation].append(sentence)  

for key, values in collocation_sentences.items():
    w_c_d = key[0] + '_' + key[1] + '_' + key[2]
    first_item = w_c_d + '\t' + values[0]
    first_score = compute_score(key[0], values[0])
    max_element = (first_item, first_score)
    for sent in values[1:]:
        item = w_c_d + '\t' + sent
        score = compute_score(key[0], sent)
        if max_element[1] < score:
            max_element = (item, score)  
    print(max_element[0])
