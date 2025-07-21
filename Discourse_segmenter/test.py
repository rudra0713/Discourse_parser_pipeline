import spacy, pickle

x = pickle.load(open("data/fnc_claim_article_label.p", "rb"))
print(type(x))
for key in x:
    if key == 'test_2597':
        print(key)
        print(x[key])
        break


# x = pickle.load(open("output/fnc_claim_with_articles_edus.p", "rb"))
# print(type(x))
# for key in x:
#     print(key)
#     print(x[key])
#
#     break
# print(len(x))