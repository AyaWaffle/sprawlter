import calc_pen as pen


def main(pkl_path): 
    # get_object: pklファイルのpathを受け取ったら、展開してobjectで返す
    object1 = pen.get_object(pkl_path)
    meta_node_info = pen.calc_meta_node(object1["ori"])

    # calculate penalty (first)
    print("-------- first time ---------")
    pen.calcPenaltyOneGraph(object1, 1,  meta_node_info)
    # calculate penalty (second)
    print("-------- second time ---------")
    pen.calcPenaltyOneGraph(object1, 2, meta_node_info)