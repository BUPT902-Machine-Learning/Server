from textCoreAlgorithm.algorithm_CNN.cnn_model import TCNNConfig
from textCoreAlgorithm.algorithm_RNN.rnn_model import TRNNConfig


def cnn_set(params):
    config = TCNNConfig()
    config.seq_length = params["seq_length"]
    config.num_classes = params["num_classes"]

    if params["embedding_dim"] != '-1':
        config.embedding_dim = int(params["embedding_dim"])
    if params["num_filters"] != '-1':
        config.num_filters = int(params["num_filters"])
    if params["kernel_size"] != '-1':
        config.kernel_size = int(params["kernel_size"])
    if params["fully_connected_dim"] != '-1':
        config.hidden_dim = int(params["fully_connected_dim"])
    if params["dropout_keep_prob"] != '-1':
        config.dropout_keep_prob = int(params["dropout_keep_prob"])
    if params["batch_size"] != '-1':
        config.batch_size = int(params["batch_size"])
    if params["num_epochs"] != '-1':
        config.num_epochs = int(params["num_epochs"])
    return config


def rnn_set(params):
    config = TRNNConfig()
    config.seq_length = params["seq_length"]
    config.num_classes = params["num_classes"]

    if params["embedding_dim"] != '-1':
        config.embedding_dim = int(params["embedding_dim"])
    if params["num_layers"] != '-1':
        config.num_layers = int(params["num_layers"])
    if params["rnn_type"] != '0':
        config.rnn_type = 'lstm'
    if params["rnn_type"] != '1':
        config.rnn_type = 'gru'
    if params["hidden_dim"] != '-1':
        config.hidden_dim = int(params["hidden_dim"])
    if params["dropout_keep_prob"] != '-1':
        config.dropout_keep_prob = int(params["dropout_keep_prob"])
    if params["batch_size"] != '-1':
        config.batch_size = int(params["batch_size"])
    if params["num_epochs"] != '-1':
        config.num_epochs = int(params["num_epochs"])
    return config


def test_cnn_set(params):
    config = TCNNConfig()
    config.seq_length = params.seq_length
    config.num_classes = params.classes_count

    if params.embedding_dim != '-1':
        config.embedding_dim = int(params.embedding_dim)
    if params.num_filters != '-1':
        config.num_filters = int(params.num_filters)
    if params.kernel_size != '-1':
        config.kernel_size = int(params.kernel_size)
    if params.fully_connected_dim != '-1':
        config.fully_connected_dim = int(params.fully_connected_dim)
    if params.dropout_keep_prob != '-1':
        config.dropout_keep_prob = int(params.dropout_keep_prob)
    if params.batch_size != '-1':
        config.batch_size = int(params.batch_size)
    if params.num_epochs != '-1':
        config.num_epochs = int(params.num_epochs)
    return config


def test_rnn_set(params):
    config = TRNNConfig()
    config.seq_length = params.seq_length
    config.num_classes = params.classes_count

    if params.embedding_dim != '-1':
        config.embedding_dim = int(params.embedding_dim)
    if params.num_layers != '-1':
        config.num_layers = int(params.num_layers)
    if params.rnn_type == '0':
        config.rnn_type = 'lstm'
    if params.rnn_type == '1':
        config.rnn_type = 'gru'
    if params.hidden_dim != '-1':
        config.hidden_dim = int(params.hidden_dim)
    if params.dropout_keep_prob != '-1':
        config.dropout_keep_prob = int(params.dropout_keep_prob)
    if params.batch_size != '-1':
        config.batch_size = int(params.batch_size)
    if params.num_epochs != '-1':
        config.num_epochs = int(params.num_epochs)
    return config
