import streamlit as st
import glob
import pandas as pd


st.title('階層型グラフ表示')
df = pd.read_csv('./sprawlter_result.csv')
# dfの表示
st.subheader("Sprawlterの算出結果")
st.dataframe(df.style.highlight_max(axis=0))

st.markdown('nnpens: nodeとnodeの重なり,　nepens: nodeとedgeの重なり,　eepens: edgeとedgeの重なり')
st.markdown('---')

# グラフの表示
st.subheader("グラフの比較表示")
graph_imgs = glob.glob('./graph_layout/*')

# container
def draw_graph(key):
    input_txt = key + ': グラフ番号(0-199)'
    graph1 = st.number_input(input_txt, min_value=0, max_value=len(graph_imgs))
    if 0 <= graph1 < len(graph_imgs):
        graph_path = "./graph_layout/graph_" + str(graph1) + ".png"
        st.image(graph_path)
    else:
        return st.error('0-99で入力')

# 上の段
upper_cols = st.columns(2)
for i in range(len(upper_cols)):
    with upper_cols[i]:
        draw_graph(str(i))

# 下の段
lower_cols = st.columns(2)
for i in range(len(lower_cols)):
    with lower_cols[i]:
        draw_graph(str(i+2))

# 29番の情報が重複(複数回計算してしまっていた)
# 最初に算出されている方を採用
# graph_29,1736.5273476774305,1295.245848483581,853.9643492897314,356.38181771801993,497.58253157171157,882.562998387699

# 大画面表示
st.markdown('---')
st.subheader("グラフの大画面表示")
draw_graph('big')