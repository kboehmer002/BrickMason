import docx
from pprint import pprint
import nltk
nltk.download('stopwords')
from Questgen import main
qe= main.BoolQGen()

doc = docx.Document('chemComputing.docx')

# Add all paragraphs to a list
full_text = []
for para in doc.paragraphs:
    full_text.append(para.text)

# Handle the text -- REPLACE: prob need to loop through paragraphs and analyze each one individually as opposed to join. Char limit for model is 512
text = {
    "input_text": " ".join(full_text)
}

# Q and A code generation code obtained at : https://github.com/ramsrigouthamg/Questgen.ai - begin quote

# Boolean questions - potential to use as an objective list and as titles in the formatted draft
output = qe.predict_boolq(text)
pprint (output)

# Multiple choice questions - append to end of draft
qg = main.QGen()
output = qg.predict_mcq(text)
pprint (output)

# Generate FAQs - also potential for section titles or objectives in the formatted draft
output = qg.predict_shortq(text)
pprint (output)

# Incorporate if possible - allows user to request rewording of a questions
oldPhrase = {
    "input_text" : "What are disadvantages of traditional computers?",
    "max_questions": 5
}
