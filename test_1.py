import pickle

x = pickle.load(open('output_data_survey_perspectrum+Abolish_nuclear_weapons_200_articles/claim_article_label.p', 'rb'))
# bracket_files = pickle.load(open('output_data_allsides+abortion_200_articles/claim_article_brackets.p', 'rb'))
# edu_files = pickle.load(open('output_data_allsides+abortion_200_articles/claim_with_articles_edus.p', 'rb'))
print(len(x))
for e in x:
    print(e)
    print(x[e])
    break
    # print(x[e])

    # break
# id_index = 'test_1'
# # b = bracket_file[id_index]
# # e = edu_file[id_index]
# discourse_tree = build_graph(edu_files[id_index], bracket_files[id_index])
# print(discourse_tree)