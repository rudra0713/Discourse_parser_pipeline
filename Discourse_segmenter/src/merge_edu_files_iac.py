import pickle, spacy

ob_1 = pickle.load(open('../data/iac_claim_with_articles_edus_100.p', 'rb'))
ob_2 = pickle.load(open('../data/iac_claim_with_articles_edus_100_400.p', 'rb'))
ob_3 = pickle.load(open('../data/iac_claim_with_articles_edus_400_rest.p', 'rb'))

ob = {}
ob.update(ob_1)
ob.update(ob_2)
ob.update(ob_3)

print("ob len: ", len(ob))

ca = pickle.load(open('../data/iac_claim_with_articles_only.p', 'rb'))
print(len(ca))

# print(ob['test_1'])
spacy_nlp = spacy.load('en')

for key in ca:
    if key not in ob:
        doc = spacy_nlp(ca[key])
        ob[key] = [sent.text for sent in list(doc.sents)]

print(len(ob))

ce = pickle.load(open('../data/iac_claim_with_articles_edus.p', 'rb'))
print("current order -> ", ce.keys())
my_order = ['test_' + str(x + 1) for x in range(len(ce))]
ce = {key: ce[key] for key in my_order}
print("new order -> ", ce.keys())
pickle.dump(ce, open("../data/iac_claim_with_articles_edus.p", "wb"))