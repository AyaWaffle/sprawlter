import pickle
import math

# nodelistのconstants
# nodelist =  [node_id, node_group, cx, cy, r, fill] のリスト
NODE_ID = 0
NODE_GROUP = 1
CX = 2
CY = 3
R = 4
FILL_COLOR = 5

def get_object(path):
    with open(path, 'rb') as f :
        object1 = pickle.load(f)
    return object1
# dict_keys(['ori', 'x_idx', 'x_ridx', 'x', 'pos', 'len', 'bounding_box', 'adj', 'graph', 'connected'])
# ori

def calc_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


# メタノードidとその半径, posを保持した辞書を作成
# meta_node = {
# {id: int,
#  nodes: int[]
#  pos: float[],
#  r: float }
# }
def calc_meta_node(ori):
    meta_node = {}
    nodelist = ori['nodelist']

    # node_groupごとに集計
    for node_id,node_group,_,_,_,_ in nodelist:
        if node_group not in meta_node.keys():
            # print('--------- make meta node No. ' + str(node_group) + '-----------------')
            meta_node[node_group]= {
                "nodes": [],
                "pos": [],
                "r": 0.0
            }
        meta_node[node_group]["nodes"].append(node_id)

    for node_group in meta_node.keys():
        minx = 1.0e+30
        miny = 1.0e+30
        maxx = -1.0e+30
        maxy = -1.0e+30

        # メタノードにノードが一つしか属さない場合
        if len(meta_node[node_group]["nodes"]) == 1:
            node_id = meta_node[node_group]["nodes"][0]
            node = nodelist[node_id]
            # nodeの情報をmeta_node辞書に格納
            meta_node[node_group]["pos"] = [node[CX], node[CY]]
            meta_node[node_group]["r"] = float(node[R])
        else:
            # メタノードの中で、最小のx、y を算出
            for node in meta_node[node_group]["nodes"]:
                x = nodelist[node][CX]
                y = nodelist[node][CY]
                minx = minx if minx < x else x
                miny = miny if miny < y else y
                maxx = maxx if maxx > x else x
                maxy = maxy if maxy > y else y
            
            centerX = (maxx + minx) / 2.0
            centerY = (maxy + miny) / 2.0

            # 算出結果をmeta_node辞書に格納
            meta_node[node_group]["pos"] = [centerX, centerY]
                #meta_nodeの半径は、中心の座標と遠くの座標の距離 + nodeの半径
            meta_node[node_group]["r"] = calc_distance((centerX, centerY), (maxx, maxy)) + (nodelist[node][R])



    return meta_node