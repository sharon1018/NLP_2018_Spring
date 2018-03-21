
# coding: utf-8

# #### NLP_HW2_20170306

# In[311]:

import re
from collections import Counter
from pprint import pprint

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('C:/Users/asus/Downloads/nlp/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of 'word'."
    return WORDS[word] / N

def correction(word):
    states = [ ("", word, 0, 0) ]
    for i in range(len(word)):
        states = [ states for state in states for states in next_states(state)]
        states = list(set(states))
        states = sorted(states, key=lambda x: (x[2],x[3]*(-1)))[:500]
    return pprint(sorted(states, key=lambda x: x[3]*(-1))[:3])

def next_states(state):
    L, R, edit, prob = state
    if len(R)>0:
        R0, R1 = R[0], R[1:]       
        if edit == 2: 
            return [state]
        else:
            letters = 'abcdefghijklmnopqrstuvwxyz'
            noedit = [( L + R0, R1, edit,  P(L + R0 + R1) )]
            delete = [( L + '', R1, edit+1,  P(L + '' + R1) )]
            replace = [(L + w , R1, edit+1, P(L + w + R1)) for w in letters]
            insert = [(L + R0 + w , R1, edit+1, P(L + R0 + w + R1)) for w in letters]
            
            return noedit+delete+replace+insert



# # In[370]:

# word='appearant'
# print('word = {}'.format(word))
# pprint(correction(word))


# # In[372]:

# word='beleive'
# print('word = {}'.format(word))
# pprint(correction(word))

