#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Yizhong
# created_at: 03/05/2018 2:57 PM
import os
import time
import logging
import numpy as np
import tensorflow as tf
import pickle
# import tensorflow.contrib as tc
tf.compat.v1.disable_eager_execution()


class BaseSegModel(object):
    def __init__(self, args, word_vocab):
        # logging
        print("inside __init__ method of base_seg.py")
        self.logger = logging.getLogger("SegEDU")

        # basic config
        self.hidden_size = args.hidden_size
        self.window_size = args.window_size
        self.optim_type = args.optim
        self.learning_rate = args.learning_rate
        self.weight_decay = args.weight_decay
        self.max_grad_norm = args.max_grad_norm
        self.dropout_keep_prob = args.dropout_keep_prob
        self.use_ema = args.ema_decay > 0

        # the vocabs
        self.word_vocab = word_vocab

        # session info
        # sess_config = tf.ConfigProto()
        sess_config = tf.compat.v1.ConfigProto()
        sess_config.gpu_options.allow_growth = True
        # self.sess = tf.Session(config=sess_config)
        self.sess = tf.compat.v1.Session(config=sess_config)

        start_t = time.time()
        # self.global_step = tf.Variable(0, name='global_step', trainable=False)
        self.global_step = tf.compat.v1.Variable(0, name='global_step', trainable=False)
        self.vars_in_checkpoint = tf.compat.v1.train.list_variables(os.path.join('Discourse_segmenter/data/models/', 'best'))
        print("vars in checkpoint: ", self.vars_in_checkpoint)
        self.all_params = tf.compat.v1.trainable_variables()

        self.vars_to_restore = {checkpoint_name: graph_var
                                for checkpoint_name, _ in self.vars_in_checkpoint
                                for graph_var in tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
                                if checkpoint_name.endswith(graph_var.name.split(":")[0]) and
                                not checkpoint_name.startswith('backup')}

        print(".............................")
        # Remove None values from the dictionary
        self.vars_to_restore = {key: val for key, val in self.vars_to_restore.items() if key is not None}
        print("vars_to_restore: ", self.vars_to_restore)

        #build-graph should be here

        self._build_graph()
        param_num = sum([np.prod(self.sess.run(tf.shape(v))) for v in self.all_params])
        self.logger.info('There are {} parameters in the model'.format(param_num))

        if self.use_ema:
            self.logger.info('Using Exp Moving Average to train the model with decay {}.'.format(args.ema_decay))
            self.ema = tf.train.ExponentialMovingAverage(decay=args.ema_decay, num_updates=self.global_step)
            self.ema_op = self.ema.apply(self.all_params)
            with tf.control_dependencies([self.train_op]):
                self.train_op = tf.group(self.ema_op)
            # with tf.variable_scope('backup_variables'):
            with tf.compat.v1.variable_scope('backup_variables'):

                self.bck_vars = [tf.get_variable(var.op.name, dtype=var.value().dtype, trainable=False,
                                                 initializer=var.initialized_value()) for var in self.all_params]
            self.ema_backup_op = tf.group(*(tf.assign(bck, var.read_value())
                                            for bck, var in zip(self.bck_vars, self.all_params)))
            self.ema_restore_op = tf.group(*(tf.assign(var, bck.read_value())
                                             for bck, var in zip(self.bck_vars, self.all_params)))
            self.ema_assign_op = tf.group(*(tf.assign(var, self.ema.average(var).read_value())
                                            for var in self.all_params))



        # initialize the model
        # all_variables = tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
        # print("all variables: ", [v.name for v in all_variables])

        # # Create a dictionary mapping variable names to their tensors in the current graph
        # current_graph_vars = {var.name: var for var in
        #                       tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)}
        # print("current_graph_vars: ", current_graph_vars)
        # # Filter variables that are present in the checkpoint
        # vars_to_restore = {name: current_graph_vars[name] for name, shape in self.vars_in_checkpoint if
        #                    name in current_graph_vars}
        # print("vars_to_restore: ", vars_to_restore)
        # Create a mapping between hierarchical names in the checkpoint and names in the current graph
        # name_mapping = {checkpoint_name: graph_var.name for checkpoint_name, _ in self.vars_in_checkpoint
        #                 for graph_var in tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
        #                 if checkpoint_name.endswith(graph_var.name.split(":")[0])}

        # print("name_mapping ... : ", name_mapping)
        # name_mapping.get(checkpoint_name, None)
        # checkpoint_vars = {checkpoint_name.split(":")[0]: tf.train.load_variable(
        #     os.path.join('Discourse_segmenter/data/models/', 'best'), checkpoint_name)
        #                    for checkpoint_name in vars_to_restore.keys()}

        print("about to run self.sess")

        # self.sess.run(tf.compat.v1.global_variables_initializer())
        # added by me
        all_variables = tf.compat.v1.get_collection_ref(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES)
        self.sess.run(tf.compat.v1.variables_initializer(all_variables))
        # self.sess.run(tf.compat.v1.variables_initializer(vars_to_restore.values()))
        self.logger.info('Time to build graph: {} s'.format(time.time() - start_t))

        # save info
        self.result_dir = args.result_dir
        if not os.path.join(self.result_dir):
            os.makedirs(self.result_dir)
        self.model_dir = args.model_dir
        if not os.path.join(self.model_dir):
            os.makedirs(self.model_dir)
        # self.saver = tf.train.Saver()

        # self.saver = tf.compat.v1.train.Saver()
        # added by me
        self.saver = tf.compat.v1.train.Saver(var_list=self.vars_to_restore)
        # self.ckpt_state = tf.compat.v1.train.get_checkpoint_state(os.path.join('Discourse_segmenter/data/models/', 'best'))
        # print('Loading checkpoint %s' % self.ckpt_state.model_checkpoint_path)
        # tf.compat.v1.train.init_from_checkpoint(os.path.join('Discourse_segmenter/data/models/', 'best'),
        #                                         assignment_map=checkpoint_vars)

    def _build_graph(self):
        raise NotImplementedError

    def _create_optimizer(self, optim_type, learning_rate):
        print("optim type: ", optim_type)
        if optim_type == 'adagrad':
            self.optimizer = tf.train.AdagradOptimizer(learning_rate)
        elif optim_type == 'adam':
            # self.optimizer = tf.train.AdamOptimizer(learning_rate)
            # self.optimizer = tf.optimizers.Adam()
            self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate)
        elif optim_type == 'rprop':
            self.optimizer = tf.train.RMSPropOptimizer(learning_rate)
        elif optim_type == 'adadelta':
            self.optimizer = tf.train.AdadeltaOptimizer(learning_rate)
        elif optim_type == 'sgd':
            self.optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        else:
            raise NotImplementedError('Unsupported optimizer: {}'.format(optim_type))

    # def _get_train_op(self, loss):
    #     print("all attributes inside _get_train_op: ", self.__dict__)
    #     self._create_optimizer(self.optim_type, self.learning_rate)
    #     # grads, vars = zip(*self.optimizer.compute_gradients(loss))
    #     # the block with "with" block is my added code
    #     # with tf.GradientTape(persistent=True) as tape:
    #     #     grads, vars = zip(*self.optimizer.compute_gradients(loss, var_list=None, tape=tape))
    #     # grads, vars = zip(*self.optimizer.compute_gradients(loss, var_list=None, tape=tf.GradientTape(persistent=True)))
    #     with tf.GradientTape(persistent=True) as tape:
    #         grads = tape.gradient(loss, self.all_params)
    #         if self.max_grad_norm:
    #             grads, grad_norm = tf.clip_by_global_norm(grads, self.max_grad_norm)
    #         else:
    #             grad_norm = tf.global_norm(grads)
    #         # train_op = self.optimizer.apply_gradients(zip(grads, vars), global_step=self.global_step)
    #         # train_op = self.optimizer.apply_gradients(zip(grads, self.all_params), global_step=self.global_step)
    #         train_op = self.optimizer.apply_gradients(zip(grads, self.all_params))
    #
    #     return grads, grad_norm, train_op

    def _get_train_op(self, loss):
        print("all attributes inside _get_train_op: ", self.__dict__)
        self._create_optimizer(self.optim_type, self.learning_rate)
        # grads, vars = zip(*self.optimizer.compute_gradients(loss))
        # the block with "with" block is my added code
        # with tf.GradientTape(persistent=True) as tape:
        #     grads, vars = zip(*self.optimizer.compute_gradients(loss, var_list=None))
        # grads, vars = zip(*self.optimizer.compute_gradients(loss, var_list=None, tape=tf.GradientTape(persistent=True)))
        # with tf.GradientTape(persistent=True) as tape:
        #     grads = tape.gradient(loss, self.all_params)
        grads, varss = zip(*self.optimizer.compute_gradients(loss, var_list=None))
        if self.max_grad_norm:
            grads, grad_norm = tf.clip_by_global_norm(grads, self.max_grad_norm)
        else:
            grad_norm = tf.global_norm(grads)
        train_op = self.optimizer.apply_gradients(zip(grads, varss), global_step=self.global_step)
            # train_op = self.optimizer.apply_gradients(zip(grads, self.all_params), global_step=self.global_step)
            # train_op = self.optimizer.apply_gradients(zip(grads, self.all_params))

        return grads, grad_norm, train_op

    def train(self, dataset, epochs, batch_size, print_every_n_batch=0):
        best_perf = None
        for epoch in range(1, epochs + 1):
            self.logger.info('Training the model for epoch {}'.format(epoch))
            train_batches = dataset.gen_mini_batches(batch_size, train=True, shuffle=True)
            train_loss = self._train_epoch(train_batches, print_every_n_batch)
            self.logger.info('Average train loss: {}'.format(train_loss))

            self.logger.info('Evaluating the model for epoch {}'.format(epoch))
            dev_batches = dataset.gen_mini_batches(batch_size, dev=True, shuffle=False)
            test_batches = dataset.gen_mini_batches(batch_size, test=True, shuffle=False)
            dev_perf = self.evaluate(dev_batches, print_every_n_batch)
            self.logger.info('Dev Precision: {}, Recall: {}, F1: {}'.format(
                dev_perf['precision'], dev_perf['recall'], dev_perf['f1']))
            test_perf = self.evaluate(test_batches, print_every_n_batch)
            self.logger.info('Test Precision: {}, Recall: {}, F1: {}'.format(
                test_perf['precision'], test_perf['recall'], test_perf['f1']))
            if best_perf is None or dev_perf['f1'] > best_perf['f1']:
                self.save('best')
                best_perf = dev_perf

    def _train_epoch(self, train_batches, print_every_n_batch):
        raise NotImplementedError

    def evaluate(self, eval_batches, print_every_n_batch=0, print_result=False):
        if self.use_ema:
            self.sess.run(self.ema_backup_op)
            self.sess.run(self.ema_assign_op)
        total_cnt, pred_cnt, correct_cnt = 0, 0, 0
        for batch_idx, batch in enumerate(eval_batches):
            if print_every_n_batch > 0 and (batch_idx + 1) % print_every_n_batch == 0:
                self.logger.info('Segmenting batch {}...'.format(batch_idx + 1))
            try:
                pred_batch_segs = self.segment(batch)
            except Exception:
                self.logger.error('Batch length is too short!')
                continue
            for sample, pred_segs in zip(batch['raw_data'], pred_batch_segs):
                gold_segs = sample['edu_seg_indices']
                total_cnt += len(gold_segs)
                pred_cnt += len(pred_segs)
                correct_cnt += len(set(gold_segs) & set(pred_segs))
                if print_result and set(gold_segs) != set(pred_segs):
                    gold_seg_words = []
                    pred_seg_words = []
                    for word_idx, word in enumerate(sample['words']):
                        if word_idx in gold_segs:
                            gold_seg_words.append('||')
                        if word_idx in pred_segs:
                            pred_seg_words.append('||')
                        gold_seg_words.append(word)
                        pred_seg_words.append(word)
                    self.logger.info('='*10)
                    self.logger.info('Gold EDU seg: {}'.format(' '.join(gold_seg_words)))
                    self.logger.info('Pred EDU seg: {}'.format(' '.join(pred_seg_words)))
                    self.logger.info('=' * 10)
        perf = {'precision': 1.0 * correct_cnt / pred_cnt if pred_cnt > 0 else 0.0,
                'recall': 1.0 * correct_cnt / total_cnt if total_cnt > 0 else 0.0}
        if perf['precision'] > 0 and perf['recall'] > 0:
            perf['f1'] = 2.0 * perf['precision'] * perf['recall'] / (perf['precision'] + perf['recall'])
        else:
            perf['f1'] = 0
        if self.use_ema:
            self.sess.run(self.ema_restore_op)
        return perf

    def segment(self, batch):
        raise NotImplementedError

    def save(self, model_name, save_dir=None):
        if save_dir is None:
            save_dir = self.model_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.saver.save(self.sess, os.path.join(save_dir, model_name))
        self.logger.info('Model saved with name: {}.'.format(model_name))

    def restore(self, model_name, restore_dir=None):
        if restore_dir is None:
            restore_dir = self.model_dir
        # temp_saver.restore(sess, ckpt_state.model_checkpoint_path)

        self.saver.restore(self.sess, os.path.join(restore_dir, model_name))
        # self.saver.restore(self.sess, self.ckpt_state.model_checkpoint_path)
        self.logger.info('Model restored from {}'.format(os.path.join(restore_dir, model_name)))