#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yizhong
# created_at: 16-11-28 下午2:48

import argparse
import os
from utils.xmlreader import reader, writer, combine
import pickle, sys


def join_edus(fedu):
    ftext = fedu.replace('.edus', '.text')
    with open(fedu, 'r') as fin, open(ftext, 'w') as fout:
        lines = [l.strip() for l in fin if l.strip()]
        fout.write(' '.join(lines))


def extract(fxml):
    sent_list, const_list = reader(fxml)
    sent_list = combine(sent_list, const_list)
    fconll = fxml.replace(".text.xml", ".conll")
    writer(sent_list, fconll)


def merge(fxml):
    fconll = fxml.replace('.text.xml', '.conll')
    fedu = fxml.replace('.text.xml', '.edus')
    fmerge = fxml.replace('.text.xml', '.merge')
    fpara = fxml.replace('.text.xml', '')
    with open(fconll, 'r') as fin1, open(fedu, 'r') as fin2, open(fpara, 'r') as fin3, open(fmerge, 'w') as fout:
        edus = [l.strip() for l in fin2 if l.strip()]
        paras = []
        para_cache = ''
        for line in fin3:
            if line.strip():
                para_cache += line.strip() + ' '
            else:
                paras.append(para_cache.strip())
                para_cache = ''
        if para_cache:
            paras.append(para_cache)
        # print("paras ", paras)
        # print("len of paras ", len(paras))
        edu_idx = 0
        para_idx = 0
        # print("edus id index 0 ", edus[edu_idx])

        cur_edu_offset = len(edus[edu_idx]) - 1 + 1  # plus 1 for one blank space
        edu_cache = ''
        for line in fin1:
            if not line.strip():
                continue
            # print("line ", line)
            line_info = line.strip().split()
            token_end_offset = int(line_info[-1])
            fout.write('%s\t%s\t%s\n' % ('\t'.join(line.strip().split('\t')[:-2]), edu_idx + 1, para_idx + 1))
            # print("token end offset ", token_end_offset)
            # print("cur edu offset ", cur_edu_offset)
            if token_end_offset == cur_edu_offset:
                edu_cache += edus[edu_idx] + ' '
                if para_idx < len(paras) and len(edu_cache) == len(paras[para_idx]) + 1:
                    edu_cache = ''
                    # print("len of paras para idx ", para_idx, len(paras[para_idx]))

                    para_idx += 1
                    # print("para idx ", para_idx)
                edu_idx += 1
                if edu_idx < len(edus):
                    cur_edu_offset += len(edus[edu_idx]) + 1
                    # print("cur edu offset inside if", cur_edu_offset)

            elif token_end_offset > cur_edu_offset:
                print("Error while merging token \"{}\" in file {} with edu : {}.".format(line_info[2], fconll,
                                                                                         edus[edu_idx]))
                edu_idx += 1
                if edu_idx < len(edus):
                    cur_edu_offset += len(edus[edu_idx]) + 1
                    # Only one error occurs when pre-processing:
                    # Error while merging token "..." in file /TRAINING/wsj_1373.out.conll with edu :
                    # that recognize facial features..


def arg_parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--data_dir', required=False, help='path to data directory.', default='../TEST')
    # parser.add_argument('--corenlp_dir', required=False, help='path to Stanford Corenlp directory.', default='/Users/rudra/PycharmProjects/StageDP-master/stanford-corenlp-full-2018-10-05')
    parser.add_argument('--data_dir', required=False, help='path to data directory.', default='../My_data_18')
    parser.add_argument('--corenlp_dir', required=False, help='path to Stanford Corenlp directory.', default='../stanford-corenlp-full-2018-10-05')

    return parser.parse_args()


def main():
    args = arg_parse()
    print("data dir ", args.data_dir)
    # sys.exit(0)

    # edu_files = [os.path.join(args.data_dir, fname) for fname in os.listdir(args.data_dir) if fname.endswith('.edus')]
    # print("edu files ...")
    # print(len(edu_files))
    # for fedu in edu_files:
    #     join_edus(fedu)
    print('Parse the *.text files...')
    os.system('bash ' + os.path.join(args.corenlp_dir, 'run_corenlp_org.sh') + ' ' + args.data_dir)

    print('Merge parsed files to generate *.merge file...')
    parse_files = [os.path.join(args.data_dir, fname) for fname in os.listdir(args.data_dir) if fname.endswith(".xml")]
    print("parse files ..")
    print(len(parse_files))
    for k, fxml in enumerate(parse_files):
        print('Processing file: {}'.format(fxml))
        extract(fxml)
        merge(fxml)
        print("done ", k)


if __name__ == '__main__':
    main()
