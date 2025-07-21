import pickle

article_files = pickle.load(open("cd_articles_only.p", "rb"))
edu_files = pickle.load(open("cd_articles_edus.p", "rb"))

del article_files['train38897']
del article_files['train49540']

del edu_files['train38897']
del edu_files['train49540']

pickle.dump(article_files, open("cd_articles_only_new.p", "wb"))
pickle.dump(edu_files, open("cd_articles_edus_new.p", "wb"))
