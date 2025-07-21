import pickle

ca = pickle.load(open('../data/iac_claim_with_articles_only.p', 'rb'))
ce = pickle.load(open('../data/iac_claim_with_articles_edus.p', 'rb'))

str = "He was in effect mocking"
count = 0
for key in ca:
    # print(x[key])
    count += 1
    if str in ca[key]:
        print(key)
x = []
for key in ce:
    if len(ce[key]) >= 1000:
        print("key -> ", key)
    x.append(len(ce[key]))

x.sort()
print(x)