from featureforge.feature import input_schema, output_schema
from featureforge.vectorizer import Vectorizer
from nltk import word_tokenize, pos_tag, wordnet
from nltk.stem.wordnet import WordNetLemmatizer

from literal_ner import LiteralNER

wnl = WordNetLemmatizer()
lner = LiteralNER()

def _wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.wordnet.NOUN
    else:
        return wordnet.wordnet.ADV


# @input_schema({'question': unicode})
# @output_schema(list(str), lambda l: len(l) > 0)
def postags(question):
    words = word_tokenize(question)
    return [pos for word, pos in pos_tag(words)]


def lemmas(question):
    words = word_tokenize(question)
    return [str(wnl.lemmatize(w, pos=_wordnet_pos(p)))
            for w, p in pos_tag(words)]


def literal_ner(question):
    ner_tuple = lner.find_ne(question)
    if ner_tuple:
        return [ner_tuple[0]] + ner_tuple[1]
    else:
        return ['No_NER']


def get_features():
    return Vectorizer([postags, lemmas, literal_ner], sparse=True)