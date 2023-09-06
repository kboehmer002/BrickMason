import re
import nltk
import string
import spacy
from negspacy.negation import Negex
from summa import summarizer

wn = nltk.WordNetLemmatizer()
ps = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('sentencizer')
nlp.add_pipe("negex", config={"ent_types":["PERSON","PRODUCT"]})

doc = nlp("She likes Sam, but not Bob.")

for e in doc.ents:
	print(e.text, e._.negex)

'''Outputs objects preceeded by negations'''
def isNegated(sentence):
    negatedEntities = [ne for ne in sentence.ents if ne._.negex]
    return negatedEntities

NE = isNegated(doc)  
print(NE)     

def summaSimmSentences(document):
    
# ----------------------------------------------      
'''Detects Similar Sentences - ei redundancies - returns T/F'''
def isRedundantSentence(sentence1, sentence2, threshold):
    sentence1 = nlp(sentence1)
    sentence2 = nlp(sentence2)
    return sentence1.similarity(sentence2) > threshold

# --------------------------------------------

'''Returns lists of lists of redundant sentences. Sentence being compared is returned first in all caps. Red sents are in sentence case in the same list.'''
def returnRedundantSentences(document, threshold):
    
    document = nlp(document)
    
    redundantSentences = []
    
    for sentenceA in document.sents:
        
        rs = []
        
        for sentenceB in document.sents:
            if sentenceA.text is not sentenceB.text and sentenceA.similarity(sentenceB) > threshold:
                rs.append(sentenceB)
        if rs:
            redundantSentences.append([sentenceA.text.upper()] + [r.text for r in rs])
    return redundantSentences

# -----------------------------------------------------------------------------

document = "The cat in the hat is black. The cat in the hat is dark black. The dog is blue. The cat is blue. The cat in the hat is blue."
result = returnRedundantSentences(document, 0.90)
print(result)

# -----------------------------------------------------------------------------

'''Find all words in a sentence'''
def findWords(text):
    return re.findall('\w+', text)

# -----------------------------------------------------------------------------

'''Remove punctuation from a sentence'''
def removePunctuation(text):
    text_nopunct = "".join([word for word in text if word not in string.punctuation])
    return text_nopunct

# -----------------------------------------------------------------------------

'''Return list of important words in the text'''
def cleanText(text):
    text = removePunctuation(text)
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word not in stopwords]
    return text

# -----------------------------------------------------------------------------

'''Stem a list of tokens'''
def stemText(tokens):
    text = [ps.stem(word) for word in text]
    return text

# -----------------------------------------------------------------------------

'''Lemmatizes a list of tokens'''
def lemmatizeText(tokens):
    text = [wn.lemmatize(word) for word in tokens]
    return text
# --------------------------------------------------------------------------------------

def to_set(*strings):
    return set(strings)

def strings_to_list(*strings):
    result = []
    for string in strings:
        result += list(string)
    return result

def string_to_set(string):
    return {string}

def string_to_list(string):
    return [string]

'''accepts variable amount of strings and returns as ordered list of strings'''
def ordered_list_of_strings(*strings):
    return list(strings)
