""" Utils for Model handling / training """
import csv
import os

from tensorflow.python.keras.models import Model

from data.utils import copy_file


def find_the_best_id_in_log(log_file_path, metric, id='epoch', offset=-1):
    """ Returns the path of the best model """
    if not os.path.exists(log_file_path):
        raise FileExistsError("File %s does not exist" % log_file_path)

    epoch_results = dict()
    with open(log_file_path, newline='') as logfile:
        reader = csv.reader(logfile, delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                metric_col = row.index(metric)
                id_col = row.index(id)
            else:
                epoch_results[row[id_col]] = float(row[metric_col])

    best_model_id = min(epoch_results, key=epoch_results.get)
    return best_model_id


def find_model_based_on_epoch(model_path, epoch, offset=-1):
    """ Returns path to the best model """
    epoch = str(int(epoch) + offset)
    files = [file_dir for file_dir in os.listdir(model_path)
             if os.path.isfile(os.path.join(model_path, file_dir))]
    all_model_files = [x for x in files if x.endswith('.hdf5')]
    search_string = 'epoch_' + epoch
    models_to_find = [x for x in all_model_files if search_string in x]
    path_to_models_to_find = [model_path + x for x in models_to_find]
    return path_to_models_to_find


def copy_models_and_config_files(model_source, model_target,
                                 files_path_source,
                                 files_path_target, copy_files=".json"):
    """ copy model from source to target and all config files """

    files = [file_dir for file_dir in os.listdir(files_path_source)
             if os.path.isfile(os.path.join(files_path_source, file_dir))]
    files_to_copy = [x for x in files if x.endswith(copy_files)]

    for file in files_to_copy:
        file_path = os.path.join(files_path_source, file)
        target_path = os.path.join(files_path_target, file)
        copy_file(file_path, target_path)

    copy_file(model_source, model_target)


def is_multi_gpu_model(model):
    """ Check if a specific model is a multi_gpu model by checking if one of
        the layers is a keras model itself
    """
    for layer in model.layers:
        if isinstance(layer, Model):
            return True
    return False


def get_gpu_base_model(model):
    """ get multi_gpu base model
    """
    for layer in model.layers:
        if isinstance(layer, Model):
            return layer
    return None
