#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yizhong
# created_at: 10/27/2016 下午8:04
import os, pickle

from eval.metrics import Metrics
from models.parser import RstParser
from models.tree import RstTree
from utils.document import Doc
import sys


cd_articles_brackets = {}


class Evaluator(object):
    def __init__(self, model_dir='Discourse_parser/data/model'):
        print('Load parsing models ...')
        self.parser = RstParser()
        self.parser.load(model_dir)

    def parse(self, doc):
        """ Parse one document using the given parsing models"""
        pred_rst = self.parser.sr_parse(doc)
        return pred_rst

    @staticmethod
    def writebrackets(fname, brackets):
        """ Write the bracketing results into file"""
        # print('Writing parsing results into file: {}'.format(fname))
        bracket_file_name = fname[fname.rindex("/") + 1: fname.index('.', fname.rindex("/") + 1)]
        print(bracket_file_name)
        # print(fname.index("."))
        # print(os.path.splitext(fname)[0])
        cd_articles_brackets[bracket_file_name] = brackets
        # with open(fname, 'w') as fout:
        #     for item in brackets:
        #         print("item -> ", item)
        #         fout.write(str(item) + '\n')

    def eval_parser(self, path='./examples', report=False, bcvocab=None, draw=False, output_dir='', output_file=''): # changed draw to false by rudra
        """ Test the parsing performance"""
        # Evaluation
        met = Metrics(levels=['span', 'nuclearity', 'relation'])
        # ----------------------------------------
        # Read all files from the given path
        doclist = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.merge')]
        pred_forms = []
        gold_forms = []
        depth_per_relation = {}
        count_merge = 0
        print("len of doclist ", len(doclist), path)
        for fmerge in doclist:
            count_merge += 1
            # ----------------------------------------
            # Read *.merge file
            doc = Doc()
            doc.read_from_fmerge(fmerge)
            # ----------------------------------------
            # Parsing
            try:
                pred_rst = self.parser.sr_parse(doc, bcvocab)
            except:
                print("error for ", fmerge)
            if draw:
                pred_rst.draw_rst(fmerge.replace(".merge", ".ps"))
            # Get brackets from parsing results
            pred_brackets = pred_rst.bracketing()
            fbrackets = fmerge.replace('.merge', '.brackets')
            # print("fbrackets ", fbrackets)
            # Write brackets into file
            Evaluator.writebrackets(fbrackets, pred_brackets)
            # ----------------------------------------
            # Evaluate with gold RST tree
            if report:
                fdis = fmerge.replace('.merge', '.dis')
                gold_rst = RstTree(fdis, fmerge)
                gold_rst.build()
                met.eval(gold_rst, pred_rst)
                for node in pred_rst.postorder_DFT(pred_rst.tree, []):
                    pred_forms.append(node.form)
                for node in gold_rst.postorder_DFT(gold_rst.tree, []):
                    gold_forms.append(node.form)

                nodes = gold_rst.postorder_DFT(gold_rst.tree, [])
                inner_nodes = [node for node in nodes if node.lnode is not None and node.rnode is not None]
                for idx, node in enumerate(inner_nodes):
                    relation = node.rnode.relation if node.form == 'NS' else node.lnode.relation
                    rela_class = RstTree.extract_relation(relation)
                    if rela_class in depth_per_relation:
                        depth_per_relation[rela_class].append(node.depth)
                    else:
                        depth_per_relation[rela_class] = [node.depth]
                    lnode_text = ' '.join([gold_rst.doc.token_dict[tid].word for tid in node.lnode.text])
                    lnode_lemmas = ' '.join([gold_rst.doc.token_dict[tid].lemma for tid in node.lnode.text])
                    rnode_text = ' '.join([gold_rst.doc.token_dict[tid].word for tid in node.rnode.text])
                    rnode_lemmas = ' '.join([gold_rst.doc.token_dict[tid].lemma for tid in node.rnode.text])
                    # if rela_class == 'Topic-Change':
                    #     print(fmerge)
                    #     print(relation)
                    #     print(lnode_text)
                    #     print(rnode_text)
                    #     print()

        # global cd_articles_brackets
        print("key len ", len(cd_articles_brackets))
        pickle.dump(cd_articles_brackets, open(output_dir + os.sep + output_file, "wb"))
        # # print(cd_articles_brackets['train1'])
        # data_path = '/home/rrs99/scratch/StageDP-master/My_data'
        # for filename in os.listdir(data_path):
        #     if 'out' in filename:
        #         os.unlink(data_path + os.sep + filename)

        if report:
            met.report()
            # print(Counter(pred_forms))
            # print(Counter(gold_forms))
            # for relation, depths in depth_per_relation.items():
            #     print('{} {}'.format(relation, sum(depths) / len(depths)))
