#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yizhong
# created_at: 03/05/2018 2:56 PM
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import logging
import random
import numpy as np
import tensorflow as tf
import sys
from config import parse_args
# from api import prepare, train, evaluate, segment
from api_server import prepare, train, evaluate, segment
# from api_server_mp import prepare, train, evaluate, segment_mp


if __name__ == '__main__':
    args = parse_args()
    print("args ........", args)
    # sys.exit(0)
    logger = logging.getLogger("SegEDU")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if args.log_path:
        file_handler = logging.FileHandler(args.log_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.info('Running with args : {}'.format(args))

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = '0'  # changed by me
    # os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    random.seed(args.seed)
    np.random.seed(args.seed)
    tf.set_random_seed(args.seed)
    # tf.random.set_seed(args.seed)

    if args.prepare:
        prepare(args)
    if args.train:
        train(args)
    if args.evaluate:
        evaluate(args)
    if args.segment:
        segment(args)
        # segment_mp(args)
