import pickle

def get_object(path):
    with open(path, 'rb') as f :
        object1 = pickle.load(f)
    return object1
# dict_keys(['ori', 'x_idx', 'x_ridx', 'x', 'pos', 'len', 'bounding_box', 'adj', 'graph', 'connected'])
# ori:
def get_node_num(ori):
    return ori['nodelist']
