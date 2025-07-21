import pickle

x = pickle.load(open("../data/procon_claim_with_articles_only.p", "rb"))
y = pickle.load(open("../data/procon_claim_with_articles_edus.p", "rb"))
# print(y)
# for key in y:
#     print(key)

count = 0
for key in x:
    print(x[key])
    print(y[key])
    count += 1
    if count == 5:
        break
