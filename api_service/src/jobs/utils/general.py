import os
import pickle


def dump_to_pickle(data, path):
    with open(path, "wb") as file:
        pickle.dump(data, file)


def load_from_pickle(path):
    if not os.path.exists(path):
        return None
    else:
        with open(path, "rb") as file:
            data = pickle.load(file)
        return data



