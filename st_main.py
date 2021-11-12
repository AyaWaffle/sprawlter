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
st.subheader("グラフ表示")
graph_imgs = glob.glob('./graph_layout/*')
graph_num = st.number_input('グラフ番号(0-199)', min_value=0, max_value=len(graph_imgs))

if 0 <= graph_num < len(graph_imgs):
    graph_path = "./graph_layout/graph_" + str(graph_num) + ".png"
    st.image(graph_path)
else:
    st.error('0-99で入力')


# 29番の情報が重複(複数回計算してしまっていた)
# 最初に算出されている方を採用
# graph_29,1736.5273476774305,1295.245848483581,853.9643492897314,356.38181771801993,497.58253157171157,882.562998387699