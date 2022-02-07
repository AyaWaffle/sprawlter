import math, pickle

# 定数
NN_ALPHA = 0.25
NE_ALPHA = 0.25
EE_ALPHA = 0.1

NN_RATIO = 1.0
NE_RATIO = 1.0
EE_RATIO = 1.0
EE_RATIO2 = 0.5
EE_RATIO3 = 0.0
	
maxnn = 0.0
maxne = 0.0
maxee = 0.0

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

# calc distance between pos1 and pos2
def calc_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# pick up meta_node info
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
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x)
                maxy = max(maxy, y)
            
            centerX = (maxx + minx) / 2.0
            centerY = (maxy + miny) / 2.0

            # 算出結果をmeta_node辞書に格納
            meta_node[node_group]["pos"] = [centerX, centerY]
                #meta_nodeの半径は、中心の座標と遠くの座標の距離 + nodeの半径
            meta_node[node_group]["r"] = calc_distance((centerX, centerY), (maxx, maxy)) + (nodelist[node][R])

    return meta_node

# Calculate sprawl：空間の粗密度を計算
def calcSprawl(meta_node_info):
    sprawl = 0.0
    minx = 1.0e+30
    miny = 1.0e+30
    maxx = -1.0e+30
    maxy = -1.0e+30

    for i in meta_node_info.keys():
        # metaノードの情報を渡したい
        meta_node = meta_node_info[i]
        pos = meta_node["pos"]
        r =  float(meta_node["r"])
        x1 = pos[0] - r
        x2 = pos[0] + r
        y1 = pos[1] - r
        y2 = pos[1] + r

        minx = min(minx, x1)
        miny = min(miny, y1)
        maxx = max(maxx, x2)
        maxy = max(maxy, y2)

        # CHECK: グラフ全体の範囲を知りたいなら、maxx, maxyはx2, y2を使った方がイメージと近い
        # maxx = maxx if maxx > x2 else x2
        # maxy = maxy if maxy > y2 else y2

    # CHECK: sprawl = (maxx - minx) * (maxy - miny) / graph.nodes.size();の graph.nodes.size
    # metaノードの大きさ？
    sprawl = (maxx - minx) * (maxy - miny) / float(r*2)
    return sprawl

def calcNodeNodePenalty(phase, meta_node_info):
    global maxnn
    penalty = 0.0
    p0 = 0.0

    # for each vertex pair
    for i in meta_node_info.keys():
        meta_node1 = meta_node_info[i]
        pos1 = meta_node1["pos"]
        r1 =  float(meta_node1["r"])

        for j in range(i+1, len(meta_node_info.keys())):
            meta_node2 = meta_node_info[j]
            pos2 = meta_node2["pos"]
            r2 =  float(meta_node2["r"])

            # calculate distance between circles
            diffr = (r1 - r2) if r1 > r2 else r2 - r1
            
            # 二つのノードの中心間距離
            dist = calc_distance(pos1, pos2)
            
            if (r1 + r2) < dist:
                # both meta nodes are completely far from each other
                continue

            # if a circle encloses another circle
            if dist < diffr:
                # 2つのメタノードの重なりは小さい内側の円の面積と一致
                if r1 > r2:
                    p0 = math.sqrt(r2 * r2 * math.pi)
                    continue
                else:
                    p0 = math.sqrt(r1 * r1 * math.pi)
                    continue
            
            # if circles partially overlap
            else:
                # 2つのメタノードの重なりを算出
                # print('r1: ' + str(r1) +  '     r2: ' + str(r2) +  '   dist: ' + str(dist))
                cos1 = (dist * dist + r1 * r1 - r2 * r2) / (2 * dist * r1)
                cos2 = (dist * dist + r2 * r2 - r1 * r1) / (2 * dist * r2)
                p0 = r1 * r1 * math.acos(cos1) + r2 * r2 * math.acos(cos2) - 0.5 * math.sqrt(4 * dist * dist * r1 * r1 - (dist * dist + r1 * r1 - r2 * r2) * (dist * dist + r1 * r1 - r2 * r2))

            # Add the penalty
            if phase == 1:
                maxnn = max(maxnn, p0)
            else:
                p0 = (1 - NN_ALPHA) * math.pow((2.0 * p0), 0.7) + NN_ALPHA * math.pow(maxnn, 0.7)
            
            penalty += p0
    
    return penalty

# Calculate node-edge overlap penalty
def calcNodeEdgePenalty(object1, phase, meta_node_info):
    global maxne
    penalty = 0.0
    linelist = object1['ori']['linelist']
    nodelist = object1['ori']['nodelist']

    # for each edge
    # edge: edge両端のnode_id
    for edge in linelist:
        ex1 = nodelist[edge[0]][CX]
        ey1 = nodelist[edge[0]][CY]
        ex2 = nodelist[edge[1]][CX]
        ey2 = nodelist[edge[1]][CY]
        ea = ex2 - ex1
        eb = ey2 - ey1
        ec = -(ea * ex1 + eb * ey1)

        # for each vertex
        for i in meta_node_info.keys():
            meta_node = meta_node_info[i]
            c = meta_node["pos"]
            r =  float(meta_node["r"])
            D = math.fabs(ea * c[0] + eb * c[1] + ec)
            eab = ea* ea + eb * eb
            det = eab * r * r - D * D

            if det <= 0.0:
                continue
            det = math.sqrt(det)
            cx1 = c[0] + (ea * D - eb * det) / eab
            cy1 = c[1] + (eb * D + ea * det) / eab
            cx2 = c[0] + (ea * D + eb * det) / eab
            cy2 = c[1] + (eb * D - ea * det) / eab
            if cx1 > ex1 and cx1 > ex2 and cx2 > ex1 and cx2 > ex2:
                continue
            if cx1 < ex1 and cx1 < ex2 and cx2 < ex1 and cx2 < ex2:
                continue
            len = calc_distance((cx1, cy1), (cx1, cy2))

            if(phase == 1):
                maxne = max(maxne, len)
            else:
                len = 2.0 * (1.0 - NE_ALPHA) * len + NE_ALPHA * maxne
            penalty += len

    return penalty

# Calculate edge-edge overlap penalty
def calcEdgeEdgePenalty(object1):
    PENALTY_CONST = 1.0
    penalty = 0.0
    linelist = object1['ori']['linelist']
    nodelist = object1['ori']['nodelist']

    # for each edge pair
    for i, edge1 in enumerate(linelist):
        x11 = nodelist[edge1[0]][CX]
        y11 = nodelist[edge1[0]][CY]
        x12 = nodelist[edge1[1]][CX]
        y12 = nodelist[edge1[1]][CY]
        x1v = x12 - x11
        y1v = y12 - y11
        # edgeの長さを三平方で計算
        len1 = math.sqrt(x1v * x1v + y1v * y1v)

        for j in range(i+1, len(linelist)):
            edge2 = linelist[j]
            x21 = nodelist[edge2[0]][CX]
            y21 = nodelist[edge2[0]][CY]
            x22 = nodelist[edge2[1]][CX]
            y22 = nodelist[edge2[1]][CY]
            
            # check the intersection: 交差があるか検証
            s = (x11 - x12) * (y21 - y11) - (y11 - y12) * (x21 - x11)
            t = (x11 - x12) * (y22 - y11) - (y11 - y12) * (x22 - x11)
            if s * t > 0:
                continue
            s = (x21 - x22) * (y11 - y21) - (y21 - y22) * (x11 - x21)
            t = (x21 - x22) * (y12 - y21) - (y21 - y22) * (x12 - x21)
            if s * t > 0:
                continue
			
            # calculate the inner product as the penalty
            x2v = x22 - x21
            y2v = y22 - y21
            len2 = math.sqrt(x2v * x2v + y2v * y2v)
            inner = math.fabs(x1v * x2v + y1v * y2v) / (len1 * len2) + PENALTY_CONST
            penalty += inner
    
    return penalty


# Evaluate one graph
# meta_node_infoの中でも、pos, meta_nodeのr, idがわかればOK
# pred_yはy座標のみ？
def calcPenaltyOneGraph(object1, phase, meta_node_info):
    # このパラメータ何？(もともとnormalizedに入っている)
    MIN = 1.0
    MAX = 10.0
    EPSILON = 0.001


    # 訓練データすべてのpenaltyを予め算出し、maxとminを取得
    nnmin = 0.0
    nnmax = 34355.44972
    nemin = 4013512.475
    nemax = 10176103.45
    # eemin = 1487715.243
    # eemax = 2008633.511
    
    # 引数で与えられたグラフのpenaltyをそれぞれ算出
    sprawl = calcSprawl(meta_node_info)
    nnpen = calcNodeNodePenalty(phase, meta_node_info)
    nepen = calcNodeEdgePenalty(object1, phase, meta_node_info)
    # eepen = calcEdgeEdgePenalty(object1)

    # normlizeする
    vnn = (nnpen - nnmin) / (nnmax - nnmin)
    vne = (nepen - nemin) / (nemax - nemin)
    # vee = (eepen - eemin) / (eemax - eemin)

    # もしvnn, vne, veeが負になったら、0に揃える
    vnn = vnn if vnn > 0 else 0
    vne = vne if vne > 0 else 0
    # vee = vee if vee > 0 else 0

    normalized_nnpen = math.sqrt(sprawl* vnn)
    normalized_nepen = math.sqrt(sprawl* vne)
    # normalized_eepen = math.sqrt(sprawl* vee)

    # result(Sprawlterの算出)
    # result3 = NN_RATIO * normalized_nnpen + NE_RATIO * normalized_nepen + EE_RATIO3 * normalized_eepen
    result3 = NN_RATIO * normalized_nnpen + NE_RATIO * normalized_nepen

    return result3

