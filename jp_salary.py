# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from matplotlib.font_manager import FontProperties

# %%
import warnings

warnings.simplefilter("ignore")

# %% [markdown]
# ## データ
#
# RANSAS から取得した総務省データ
#

# %%
df_jp_all = pd.read_csv("./csv_data/一人あたり賃金_全国_全産業_2010-2021.csv", encoding="utf-8")
df_jp_ind = pd.read_csv("./csv_data/一人あたり賃金_全国_産業別_2010-2021.csv", encoding="utf-8")
df_jp_category = pd.read_csv(
    "./csv_data/一人あたり賃金_全国_産業業種別_2010-2021.csv", encoding="utf-8"
)
df_pref_all = pd.read_csv("./csv_data/一人あたり賃金_都道府県_全産業_2010-2021.csv", encoding="utf-8")
df_pref_ind = pd.read_csv("./csv_data/一人あたり賃金_都道府県_産業別_2010-2021.csv", encoding="utf-8")
df_pref_category = pd.read_csv(
    "./csv_data/一人あたり賃金_都道府県_産業業種別_2010-2021.csv", encoding="utf-8"
)

# %%
print(df_jp_all.shape)
print(df_jp_all.dtypes)
df_jp_all.head(3)

# %%
print(df_jp_ind.shape)
print(df_jp_ind.dtypes)
df_jp_ind.head(3)

# %%
print(df_jp_category.shape)
print(df_jp_category.dtypes)
df_jp_category.head(3)

# %%
print(df_pref_all.shape)
print(df_pref_all.dtypes)
df_pref_all.head(3)

# %%
print(df_pref_ind.shape)
print(df_pref_ind.dtypes)
df_pref_ind.head(3)

# %%
print(df_pref_category.shape)
print(df_pref_category.dtypes)
df_pref_category.head(3)

# %% [markdown]
# ## ユニークデータ確認
#

# %%
df_pref_category["産業大分類名"].unique()

# %%
df_pref_category["産業大分類名"].nunique()

# %%
df_pref_category["年齢"].unique()

# %%
df_pref_category["年齢"].nunique()

# %%
df_pref_category["業種中分類名"].unique()

# %%
df_pref_category["業種中分類名"].nunique()

# %%
print(df_jp_all.duplicated().any())
print(df_jp_ind.duplicated().any())
print(df_jp_category.duplicated().any())
print(df_pref_all.duplicated().any())
print(df_pref_ind.duplicated().any())
print(df_pref_category.duplicated().any())

# %% [markdown]
# ## 欠損値確認
#

# %%
df_jp_all.isnull().sum()

# %%
df_jp_ind.isnull().sum()

# %%
df_jp_category.isnull().sum()

# %%
df_pref_all.isnull().sum()

# %%
df_pref_ind.isnull().sum()

# %%
df_pref_category.isnull().sum()

# %% [markdown]
# ### 集計列に特定の文字列を持つ DF の行抽出 (pref_ind, pref_category)
#
# - 直接 float にしようとすると, 以下コメントアウトされた処理はエラーになる
#   - ハイフンが入っているため float に変換できない
#

# %%
# df_pref_ind['所定内給与額（万円）'] = df_pref_ind['所定内給与額（万円）'].astype(float)

# %%
# df_pref_category['所定内給与額（万円）'] = df_pref_category['所定内給与額（万円）'].astype(float)

# %% [markdown]
# ハイフンが入っている行を抽出してみる
#
# - 企業に勤めている可能性が低い年齢層の給与額にハイフンを与えている印象
# - ハイフン一文字のみで欠損を表しているらしい
#

# %%
df_pref_category[df_pref_category["所定内給与額（万円）"] == "-"]

# %%
df_pref_category[df_pref_category["所定内給与額（万円）"] == "-"]

# %%
df_pref_category[df_pref_category["所定内給与額（万円）"].str.contains("-")]

# %% [markdown]
# ### 欠損値 DF を生成してみる
#

# %%
temp_df = df_pref_category[df_pref_category["所定内給与額（万円）"] == "-"]
temp_df.head()

# %%
temp_df["年齢"].unique()

# %%
temp_df["年齢"].value_counts()

# %% [markdown]
# - 働いてない割合が高い年齢層に欠損値が多い
#

# %%
temp_df["都道府県名"].value_counts()

# %% [markdown]
# - 失業率が高そうな都道府県に欠損値が多い
#

# %%
temp_df["産業大分類名"].value_counts()

# %% [markdown]
# - 解釈が難しい
# - 製造業で突出している
#

# %%
temp_df["業種中分類名"].value_counts()

# %% [markdown]
# - ばらつきがあり,解釈が難しい
#

# %% [markdown]
# ### 欠損値処理
#

# %%
df_pref_category["所定内給与額（万円）"] = df_pref_category["所定内給与額（万円）"].replace("-", np.nan)
df_pref_category["年間賞与その他特別給与額（万円）"] = df_pref_category["年間賞与その他特別給与額（万円）"].replace(
    "-", np.nan
)
df_pref_category["一人当たり賃金（万円）"] = df_pref_category["一人当たり賃金（万円）"].replace("-", np.nan)
df_pref_ind["所定内給与額（万円）"] = df_pref_ind["所定内給与額（万円）"].replace("-", np.nan)
df_pref_ind["年間賞与その他特別給与額（万円）"] = df_pref_ind["年間賞与その他特別給与額（万円）"].replace("-", np.nan)
df_pref_ind["一人当たり賃金（万円）"] = df_pref_ind["一人当たり賃金（万円）"].replace("-", np.nan)

df_pref_ind["所定内給与額（万円）"] = df_pref_ind["所定内給与額（万円）"].astype(float)
df_pref_category["所定内給与額（万円）"] = df_pref_category["所定内給与額（万円）"].astype(float)

# %%
df_pref_ind.isnull().sum()

# %%
df_pref_category.isnull().sum()

# %% [markdown]
# - 欠損値の集計値が変換前ハイフンの集計値と合致しているため, 全て NA となり集計可能になっている模様
#

# %% [markdown]
# | DF       | 全データ | 欠損値 | 欠損率 |
# | -------- | -------- | ------ | ------ |
# | ind      | 249288   | 20860  | 8.36%  |
# | category | 117312   | 4019   | 3.42%  |
#
# - 欠損値の割合は低い
# - 今回は全体把握するための分析なので欠損値は削除しておく,で問題なさそう
#

# %% [markdown]
# #### 欠損値削除
#

# %%
df_pref_category.dropna(subset=["所定内給与額（万円）"], axis=0, inplace=True)
df_pref_ind.dropna(subset=["所定内給与額（万円）"], axis=0, inplace=True)

# %%
df_pref_category.isnull().sum()

# %%
df_pref_ind.isnull().sum()

# %% [markdown]
# ## データ型変換
#
# 金額として集計したいが object 型になっているカラムを float 型へ変換する
#

# %%
df_pref_ind = df_pref_ind.astype(
    {"所定内給与額（万円）": float, "年間賞与その他特別給与額（万円）": float, "一人当たり賃金（万円）": float}
)
df_pref_category = df_pref_category.astype(
    {"所定内給与額（万円）": float, "年間賞与その他特別給与額（万円）": float, "一人当たり賃金（万円）": float}
)
print(df_pref_ind.dtypes)
print(df_pref_category.dtypes)

# %% [markdown]
# ## 条件抽出
#

# %%
df_pref_category[df_pref_category["一人当たり賃金（万円）"] > 400]

# %%
df_pref_category[
    (df_pref_category["都道府県名"] == "東京都") & (df_pref_category["一人当たり賃金（万円）"] > 900)
]

# %% [markdown]
# # 基礎集計
#

# %% [markdown]
# ## 全国平均賃金
#

# %%
df_jp_all.head()

# %%
df_jp_all[(df_jp_all["年齢"] == "年齢計")]

# %% [markdown]
# | カラム         | 定義          |
# | -------------- | ------------- |
# | 所定内給与額   | 基本給+諸手当 |
# | 年間賞与       | ボーナス      |
# | 一人あたり賃金 | 年間額        |
#
# 他の国の同時期の平均賃金推移を見てみたい
#

# %%
df_diff = df_jp_all[(df_jp_all["年齢"] == "年齢計")]

# %% [markdown]
# ### 一年ごとの差分を見てみる
#

# %%
df_diff["一人当たり賃金の差分（万円）"] = df_diff["一人当たり賃金（万円）"].diff()
df_diff

# %% [markdown]
# ### 各年齢層別 年度平均賃金(2010-2021)
#

# %%
df_jp_all.groupby("年齢")[["所定内給与額（万円）", "年間賞与その他特別給与額（万円）", "一人当たり賃金（万円）"]].mean()

# %% [markdown]
# - なんだかんだまだまだ年功序列傾向がすごい
# - 「給与」であることから,企業での従業員ライフサイクルがまだ決まっていることがわかる
#   - 20 代と 10 代の賃金乖離
#   - 60 代に入って急に落ち込む
#

# %% [markdown]
# ## 産業別全国平均賃金(2010-2021)
#

# %%
df_jp_ind.head()

# %%
df_jp_ind[(df_jp_ind["年齢"] == "年齢計")]

# %% [markdown]
# ### 集計結果
#

# %%
df_temp = df_jp_ind[(df_jp_ind["年齢"] == "年齢計")]
df_temp.groupby("産業大分類名")[["所定内給与額（万円）", "年間賞与その他特別給与額（万円）", "一人当たり賃金（万円）"]].mean()

# %% [markdown]
# ## 都道府県別平均賃金(2010-2021)
#

# %%
df_pref_all.head()

# %%
df_temp2 = df_pref_all[(df_pref_all["年齢"] == "年齢計")]
df_temp2

# %% [markdown]
# ### 集計結果 都道府県別平均賃金(2010-2021)
#

# %%
df_temp2.groupby("都道府県名")[
    ["所定内給与額（万円）", "年間賞与その他特別給与額（万円）", "一人当たり賃金（万円）"]
].mean().sort_values(by="一人当たり賃金（万円）", ascending=False)

# %% [markdown]
# - 一番高かった都道府県の最大賃金を記録したタイミングは 2015 年
# - つまり, 最も平均賃金が高い東京においても最大賃金記録した 2015 年から 2021 年までは下降してきていることがわかる
#

# %%
df_temp2.loc[df_temp2["一人当たり賃金（万円）"].idxmax()]

# %% [markdown]
# ## 都道府県別産業別の平均賃金
#

# %%
df_pref_ind.head()

# %%
df_temp3 = df_pref_ind[df_pref_ind["年齢"] == "年齢計"]
df_temp3

# %%
df_temp3.groupby(["都道府県名", "産業大分類名"])[
    ["所定内給与額（万円）", "年間賞与その他特別給与額（万円）", "一人当たり賃金（万円）"]
].mean().sort_values(by="一人当たり賃金（万円）", ascending=False)

# %%
df_temp3_group = (
    df_temp3.groupby(["都道府県名", "産業大分類名"])[
        ["所定内給与額（万円）", "年間賞与その他特別給与額（万円）", "一人当たり賃金（万円）"]
    ]
    .mean()
    .sort_values(by="一人当たり賃金（万円）", ascending=False)
)

# %% [markdown]
# ### 東京都における産業別平均賃金ランキング
#

# %% [markdown]
# - 専門的でない産業の賃金はやはり低い
# - 日本の平均賃金が 400 万円台といわれているので
#   - 専門的でない産業に属している人が日本人労働者の大半であることがわかる
#   - 専門的でない産業が儲かっているのであれば, 基本的に労働者へ賃金が還元されにくくなっていると考えられる
#   - 専門的でないのであれば
#     - 労働者も容易に調達可能
#     - アルバイトなど低賃金非正規労働者を雇用してコストを下げようとしている傾向が考えられる
#

# %%
df_temp3_group.loc["東京都"]

# %% [markdown]
# ---
#
# # データ可視化
#

# %% [markdown]
# matplotlib の表に日本語で表記したいので font 設定を行う
#

# %%
font_path = "./HackGen35ConsoleNF-Regular.ttf"
font_property = FontProperties(fname=font_path)

# %%
df_ts_mean = df_jp_all[(df_jp_all["年齢"] == "年齢計")].set_index("集計年")
df_ts_mean

# %%
fig = plt.figure(figsize=(10, 5))
ax = plt.axes()
ax.set_xlabel("年", fontproperties=font_property)
ax.set_ylabel("一人当たり賃金（万円）", fontproperties=font_property)
ax.plot(df_ts_mean["一人当たり賃金（万円）"])
ax.set_ylim(300, 500)
plt.show()

# %% [markdown]
# ### 年齢階級別の一人当たり賃金の箱ひげ図

# %%
print(df_pref_ind.shape)
age_list = df_pref_ind["年齢"].unique()
print(age_list)
df_pref_ind.head()

# %%
wage_list = []
for age in age_list:
    print(age)
    wage_temp = df_pref_ind[df_pref_ind["年齢"] == age]["一人当たり賃金（万円）"].values.tolist()
    wage_list.append(wage_temp)
len(wage_list)

# %%
len(wage_list[0])

# %%
fig = plt.figure(figsize=(15, 6))
ax = plt.axes()
ax.set_title("年齢階級別の一人あたり賃金", fontproperties=font_property)
ax.set_xticklabels(age_list, fontproperties=font_property)
ax.boxplot(wage_list)
plt.show()

# %% [markdown]
# - 年齢が低いほど四分位範囲が狭い
# - 年齢が高いほど四分位範囲が広く, 中央値も高くなっていく, また上限・下限境界も広い
#   - 年齢が上がるほど
#     - 賃金は高くなっていく?
#     - 65歳以降はハズレ値が大きくかなり差が開いているように見える
#     - ばらつきも大きくなる
#     - 役職につくかどうかによって大きく異なる?
#     - 専門性が高い職業についているかどうかで賃金の分岐点がある??

# %%
# 外れ値は無視する
fig = plt.figure(figsize=(15, 6))
ax = plt.axes()
ax.set_title("年齢階級別の一人あたり賃金", fontproperties=font_property)
ax.set_xticklabels(age_list, fontproperties=font_property)
ax.boxplot(wage_list, showfliers=False)
plt.show()

# %% [markdown]
# ### 産業別 一人当たり賃金(箱ひげ図)

# %%
ind_list = df_pref_ind["産業大分類名"].unique()
print(ind_list)

# %%
wage_list = []
for name in ind_list:
    print(name)
    wage_temp = df_pref_ind[df_pref_ind["産業大分類名"] == name][
        "一人当たり賃金（万円）"
    ].values.tolist()
    wage_list.append(wage_temp)

# %%
fig = plt.figure(figsize=(20, 6))
ax = plt.axes()
ax.set_title("産業別一人当たり賃金", fontproperties=font_property)
ax.set_xticklabels(ind_list, fontproperties=font_property, rotation=60)
ax.boxplot(wage_list)
plt.show()

# %% [markdown]
# - 外れ値がめちゃめちゃ多い産業が割と目につく
#   - 医療・福祉
#     - 医療従事者・福祉従事者間の差異が顕著な感じがする
#   - 金融業・保険業
#   - 鉱業・採石業

# %%
fig = plt.figure(figsize=(20, 6))
ax = plt.axes()
ax.set_title("産業別一人当たり賃金", fontproperties=font_property)
ax.set_xticklabels(ind_list, fontproperties=font_property, rotation=60)
ax.boxplot(wage_list, showfliers=False)
plt.show()
