import numpy as np
import argparse, re, pickle, os, sys
from os import listdir
from os.path import isfile, join

sys.path.insert(0, '/scratch/rrs99/Discourse_parser_pipeline')


def parse_arguments():
    parser = argparse.ArgumentParser('Discourse parsing pipeline')
    parser.add_argument('--claim', type=str, default="Marijuana should be legalized.")
    parser.add_argument('--domain_name', type=str, default="marijuana")

    return parser.parse_args()


def store_info(claim, domain_name):
    # claim = 'Abortion should be legalized.'
    # data_files = ['A1.data.rsn', 'R58.data.rsn', 'N24.data.rsn', 'U21.data.rsn', 'J23.data.rsn', 'T33.data.rsn', 'C20.data.rsn',
    #                       'U9.data.rsn', 'E1.data.rsn', 'P22.data.rsn', 'P18.data.rsn', 'Q4.data.rsn']

    folder_path = 'reason/stance/' + domain_name + '/'
    data_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith('.data')]

    claim_article_label = {}
    claim_with_articles_only = {}
    dataset_name = 'reason'
    domain_name = domain_name + '_200_articles'
    data_dir = 'output_data_' + dataset_name + '+' + domain_name
    temp_data_dir = 'temp_output_data_' + dataset_name + '+' + domain_name

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    index = 1

    for d_file in data_files:
        article_index = d_file.split('.')[0]
        f = open(folder_path + article_index + '.data', 'r', encoding='utf-8', errors='ignore')
        lines = f.readlines()
        article = lines[0].replace('\n', '')
        s = open(folder_path + article_index + '.meta', 'r', encoding='utf-8', errors='ignore')
        meta_file_lines = s.readlines()
        pid_line = meta_file_lines[1]
        # The following check makes sure that the current post is not a reply to any other test
        if '-1' not in pid_line:
            continue
        st_line = meta_file_lines[2]
        # print(st_line)
        if '+1' in st_line:
            label = 0
        else:
            label = 1
        id_index = 'test_' + str(index)
        claim_with_articles_only[id_index] = claim + " " + article
        claim_article_label[id_index] = {
            'claim': claim,
            'article': article,
            'label': label,
            'article_label': d_file
        }
        if index == 200:
            break
        index += 1

    pickle.dump(claim_article_label, open(data_dir + os.sep + 'claim_article_label.p', 'wb'))
    pickle.dump(claim_with_articles_only, open(data_dir + os.sep + 'claim_with_articles_only.p', 'wb'))
    # sys.exit(0)

    # os.system(
    #     "python3 Discourse_segmenter/src/run.py --segment  --input_files=" + data_dir + os.sep + "claim_with_articles_only.p" + " --result_dir=" + data_dir + " --result_file=claim_with_articles_edus")
    os.system(
        "python3 simple_edu_generator.py --input_files=" + data_dir + os.sep + "claim_with_articles_only.p" + " --result_dir=" + data_dir + " --result_file=claim_with_articles_edus")

    # sys.exit(0)
    os.system(
        "python3 Discourse_parser/src/create_data_files.py --article_file_path=" + data_dir + os.sep + "claim_with_articles_only.p" + " --edu_file_path=" + data_dir + os.sep + "claim_with_articles_edus.p" + " --output_dir=" + temp_data_dir)
    #
    os.system("python3 Discourse_parser/src/preprocess.py --data_dir=" + temp_data_dir)

    os.system("python3 Discourse_parser/src/main_parser.py --eval --eval_dir=" + temp_data_dir + " --output_dir=" + data_dir + " --output_file=claim_article_brackets.p")

    os.system("python3 Discourse_tree/store_ddt.py --output_dir=" + data_dir + " --bracket_file_path=claim_article_brackets.p --edu_file_path=claim_with_articles_edus.p --claim_article_file_path=claim_article_label.p --output_file=discourse_full_" + dataset_name + '+' + domain_name + '.p')
    #


if __name__ == '__main__':
    args = parse_arguments()
    # sys.exit(0)
    store_info(args.claim, args.domain_name)
