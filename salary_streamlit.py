import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px

st.title("日本の賃金情報ダッシュボード")

df_jp_all = pd.read_csv("./csv_data/一人あたり賃金_全国_全産業_2010-2021.csv", encoding="utf-8")
df_jp_ind = pd.read_csv("./csv_data/一人あたり賃金_全国_産業別_2010-2021.csv", encoding="utf-8")
# df_jp_category = pd.read_csv(
#     './csv_data/一人あたり賃金_全国_産業業種別_2010-2021.csv', encoding='utf-8'
# )
df_pref_all = pd.read_csv("./csv_data/一人あたり賃金_都道府県_全産業_2010-2021.csv", encoding="utf-8")
# df_pref_ind
# = pd.read_csv('./csv_data/一人あたり賃金_都道府県_産業別_2010-2021.csv', encoding='utf-8')
# df_pref_category = pd.read_csv(
#     './csv_data/一人あたり賃金_都道府県_産業業種別_2010-2021.csv', encoding='utf-8'
# )

st.header("■ 一人当たり平均賃金のヒートマップ（2021年度）")

jp_lat_lon = pd.read_csv("./csv_data/pref_lat_lon.csv")
jp_lat_lon = jp_lat_lon.rename(columns={"pref_name": "都道府県名"})

df_pref_map = df_pref_all[(df_pref_all["年齢"] == "年齢計") & (df_pref_all["集計年"] == 2021)]
df_pref_map = pd.merge(df_pref_map, jp_lat_lon, on="都道府県名")

# 賃金のレンジを見やすくするため正規化しておく
df_pref_map["一人当たり賃金（相対値）"] = (
    df_pref_map["一人当たり賃金（万円）"] - df_pref_map["一人当たり賃金（万円）"].min()
) / (df_pref_map["一人当たり賃金（万円）"].max() - df_pref_map["一人当たり賃金（万円）"].min())

view = pdk.ViewState(
    longitude=139.691648,
    latitude=35.689185,
    zoom=4,
    pitch=40.5,
)

layer = pdk.Layer(
    "HeatmapLayer",
    data=df_pref_map,
    opacity=0.4,
    get_position=["lon", "lat"],
    threshold=0.25,
    get_weight="一人当たり賃金（相対値）",
)

layer_map = pdk.Deck(
    layers=layer,
    initial_view_state=view,
)


st.pydeck_chart(layer_map)

show_df = st.checkbox("DataFrameを見てみる")
if show_df:
    st.write(df_pref_map)


st.header("■ 集計年別の一人当たり賃金の推移")

# 全国平均賃金推移
df_ts_mean = df_jp_all[(df_jp_all["年齢"] == "年齢計")]
df_ts_mean = df_ts_mean.rename(columns={"一人当たり賃金（万円）": "全国_一人当たり賃金（万円）"})
df_ts_mean

# 都道府県別平均賃金推移
df_pref_mean = df_pref_all[(df_pref_all["年齢"] == "年齢計")]
pref_list = df_pref_mean["都道府県名"].unique()
option_pref = st.selectbox("都道府県", (pref_list))
df_pref_mean = df_pref_mean[df_pref_mean["都道府県名"] == option_pref]
df_pref_mean

# 全国+都道府県別
df_mean_line = pd.merge(df_ts_mean, df_pref_mean, on="集計年")

# 必要な列のみ取得
df_mean_line = df_mean_line[["集計年", "全国_一人当たり賃金（万円）", "一人当たり賃金（万円）"]]
df_mean_line = df_mean_line.set_index("集計年")

# 折れ線グラフ
st.line_chart(df_mean_line)


# バブルチャート
# X: 一人当たり賃金
# Y: 賞与
# Z: 所定給与額

st.header("■ 年齢階級別の全国一人当たり平均賃金")

df_mean_bubble = df_jp_all[df_jp_all["年齢"] != "年齢計"]

fig = px.scatter(
    df_mean_bubble,
    x="一人当たり賃金（万円）",
    y="年間賞与その他特別給与額（万円）",
    range_x=[150, 700],
    range_y=[0, 150],
    size="所定内給与額（万円）",
    size_max=40,
    color="年齢",
    animation_frame="集計年",
    animation_group="年齢",
)

st.plotly_chart(fig)

# 横棒グラフ
st.header("■  産業別の賃金推移")

year_list = df_jp_ind["集計年"].unique()

# セレクトボックスで年度/賃金種別を選択できるようにする
option_year = st.selectbox("集計年", (year_list))

wage_list = ["一人当たり賃金（万円）", "年間賞与その他特別給与額（万円）", "所定内給与額（万円）"]
option_wage = st.selectbox("賃金種別", (wage_list))

df_mean_ind = df_jp_ind[(df_jp_ind["集計年"] == option_year)]

max_x = df_mean_ind[option_wage].max() + 50  # 50万分マージンをつけておく

fig = px.bar(
    df_mean_ind,
    x=option_wage,
    y="産業大分類名",
    color="産業大分類名",
    animation_frame="年齢",
    range_x=[0, max_x],
    orientation="h",
    width=800,
    height=500,
)

st.plotly_chart(fig)

st.text("出典: RESAS（地域経済分析システム）")
st.text("本結果はRESAS（地域経済分析システム）のデータを加工して作成")
