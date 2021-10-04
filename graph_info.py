import pickle

def get_object(path):
    with open(path, 'rb') as f :
        object1 = pickle.load(f)
    return object1
# dict_keys(['ori', 'x_idx', 'x_ridx', 'x', 'pos', 'len', 'bounding_box', 'adj', 'graph', 'connected'])
# ori
def calc_meta_node_r(ori):
    nodelist = ori['nodelist']
    r = 1

    return r