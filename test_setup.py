import spacy
import nltk
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
doc = nlp("John Smith is a Python developer with experience in Flask and MySQL.")

print("Named entities found:")
for ent in doc.ents:
    print(" -", ent.text, "->", ent.label_)

stop_words = stopwords.words("english")
print("\nNumber of English stopwords loaded:", len(stop_words))
print("\nspaCy and NLTK are working correctly!")