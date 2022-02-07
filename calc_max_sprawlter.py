import SprawlterEvaluator as sp
from graph_info  import *
import glob


# 単一グラフを受け取ったら、Sprawlterを計算するようにしたい
MAXNN = 1131.579792 # graph_182
MAXNE = 1133.206725 # graph_51

path =  "./sample_data2/*"
filenames = glob.glob(path)


# calculate penalty (first)
for counter, file in enumerate(filenames):
    object1 = sp.get_object(file)
    meta_node_info = sp.calc_meta_node(object1["ori"])
    # minr = 10000.0
    # for i in range(len(meta_node_info.keys())):
    #     print('----------  No. ' + str(i) + '  ---------------')
    #     # print(meta_node_info[i]["nodes"])
    #     # prCint(meta_node_info[i]["pos"])
    #     print(meta_node_info[i]["r"])
    #     minr = minr if (meta_node_info[i]["r"] > 0.1 and minr < meta_node_info[i]["r"]) else meta_node_info[i]["r"]
    # print("------- minr -----", minr)
    sp.calcPenaltyOneGraph(object1, 1, counter, meta_node_info)
    
    if counter % 1000 == 0:
        print(" #caclPenaltyOneGraph (phase 1) " + str(counter) + "/" + str(len(filenames)))

# calculate penalty (second phase)
for counter, file in enumerate(filenames):
    object1 = sp.get_object(file)
    meta_node_info = sp.calc_meta_node(object1["ori"])
    sp.calcPenaltyOneGraph(object1, 2, counter, meta_node_info)
    
    if counter % 1000 == 0:
        print(" #caclPenaltyOneGraph (phase 2) " + str(counter) + "/" + str(len(filenames)))


# normalize penalty
res = sp.normalizePenalty()

