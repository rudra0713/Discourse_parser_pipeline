# from nltk.parse.corenlp import CoreNLPParser
# st = CoreNLPParser()
# tokenized_sent = list(st.tokenize("Online debating is better. Classroom debating is not so fun."))
# # tokenized_sent = list(st.tokenize('What is the airspeed of an unladen swallow ?'))
# print(tokenized_sent)

import stanfordnlp

nlp = stanfordnlp.Pipeline(processors='tokenize', lang='en')
doc = nlp("Online debating is better. Classroom debating is not so fun.")
# sentences = list(doc.sentences)
# for sentence in sentences:
#     print(sentence)

print("---")
for i, sentence in enumerate(doc.sentences):
    sent = ' '.join(word.text for word in sentence.words)
    print(sent)
    # print(f"====== Sentence {i+1} tokens =======")
    # print(*[f"index: {token.index.rjust(3)}\ttoken: {token.text}" for token in sentence.tokens], sep='\n')