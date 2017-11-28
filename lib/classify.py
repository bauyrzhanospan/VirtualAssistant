#! /usr/bin/env python3

import os

import numpy as np
import tensorflow as tf

try:
    import data_helpers
    from text_cnn import TextCNN
except ImportError:
    from lib import data_helpers
    from lib.text_cnn import TextCNN
from tensorflow.contrib import learn
import glob

# Parameters
# ==================================================


# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("Reasons", "./lib/runs/ClassReasons/checkpoints/", "Checkpoint directory from training run")
tf.flags.DEFINE_string("Orders", "./lib/runs/ClassOrders/checkpoints/", "Checkpoint directory from training run")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()


def classifyR(x_raw):
    # print("\nParameters:")
    # for attr, value in sorted(FLAGS.__flags.items()):
    #     print("{}={}".format(attr.upper(), value))
    # print("")
    x_raw = [x_raw]
    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.Reasons, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    # print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.Reasons)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    # Save the evaluation to a csv
    memes = glob.glob('./lib/data/reasons/*[!.py]')
    scores = \
    sess.run(graph.get_operation_by_name("output/scores").outputs[0], {input_x: x_test_batch, dropout_keep_prob: 1.0})[
        0]
    if max(scores) > 2:
        return str(memes[int(all_predictions[0])])[19:]
    else:
        return None

def classifyO(x_raw):
    # print("\nParameters:")
    # for attr, value in sorted(FLAGS.__flags.items()):
    #     print("{}={}".format(attr.upper(), value))
    # print("")
    x_raw = [x_raw]
    # Map data into vocabulary
    vocab_path = os.path.join(FLAGS.Orders, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    # print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = tf.train.latest_checkpoint(FLAGS.Orders)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    # Save the evaluation to a csv
    memes = glob.glob('./lib/data/orders/*[!.py]')
    scores = \
    sess.run(graph.get_operation_by_name("output/scores").outputs[0], {input_x: x_test_batch, dropout_keep_prob: 1.0})[
        0]
    if max(scores) > 2:
        return str(memes[int(all_predictions[0])])[18:]
    else:
        return None