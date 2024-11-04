import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.imputation.mice import MICEData
from sklearn.ensemble import RandomForestRegressor
from enum_collection import Rounding
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from constant import Constant
from sklearn.preprocessing import StandardScaler


# csvファイル処理クラス
class CsvHandler:
    # 色配列
    base_color = "blue"

    # コンストラクタ
    def __init__():
        print("init")

    # データ取得
    # 1つのカラム取得
    # df[column_name]

    # 複数カラム取得
    # df[column_names]

    # データチェック
    # データ取得
    # 全カラムの指定したレコード数分表示
    # df.head(record_count)

    # データ取得（カラム指定）
    # df[labels].head(display_num)

    # 欠損値とデータ型がチェックできる
    # df.info

    # カラム表示
    # どんなカラムがあるか表示する
    # df.columns

    # 行列数
    # df.shape

    # 各カラムの値と出現回数を取得
    # df[column].value_counts()

    # 総データ数取得チェック
    # df.shape[0]

    # 各カラムの欠損値数チェック
    # df.isnull().sum()

    # 各カラムの型チェック
    # pd.DataFrame(df).dtypes

    # カラムを指定して欠損値のある行を指定
    # def get_drop_records_number(self, column):
    #     result = self._csv_data[self._csv_data[column].isnull()].index
    #     print("CsvHandler get_drop_records_number result:", result)
    #     return result

    # 行数を指定してそのレコードを取得
    # df[column].loc[record_numbers]

    # 値変換
    # ラベルエンコーディング（文字列→数値変換）
    # def label_encoder(self, column_names):
    #     print("CsvHandler label_encoder")
    #     # カラム内の値をリスト化
    #     for col in column_names:
    #         unique_values = self._csv_data[col].unique().tolist()
    #         print(f"CsvHandler label_encoder unique_values for {col} =", unique_values)

    #         # 各カラムごとに置換
    #         self._csv_data[col] = self._csv_data[col].map(
    #             lambda x: unique_values.index(x) if x in unique_values else x
    #         )

    # 標準化（平均0、分散1にスケーリング） ←これ使っておけば問題なさそう
    # StandardScaler().fit_transform(df[column_names])

    # 正規化（最小値0、最大値1スケーリング）

    # 欠損値補間
    # 行削除
    # df.drop(records_array, axis=0, inplace=True)

    # 行削除 範囲
    # df.drop(df.index[start:end], axis=0, inplace=True)

    # 列削除
    # df.drop(columns_array, axis=1, inplace=True)

    # 平均値取得（カラム指定）
    # df[column_name].mean()


# ここから未確認
# 平均値補間（カラム指定）
# df[column_name].fillna(df[column_name].mean())

# 中央値取得（カラム指定）
# df[column_name].median()

# 中央値補間（カラム指定）
# df[column_name].median()

# 最頻値取得（カラム指定）
# df[column_name].mode()[0]

# 最頻値補間（カラム指定）
# df[column_name].fillna(df[column_name].mode()[0])


# 小数点切り捨て（カラム指定）　←　平均と補完と組み合わせられないので要調査
# df[column_name].fillna(0).astype('int64')


# # 端数処理（カラム指定） ←NAN（欠損値があるとエラーになるので欠損値ない状態で処理実行のこと）
# def rounding_process(self, column_name, rounding_type, decimal_point_position):
#     print("CsvHandler rounding_process")
#     # 四捨五入処理
#     if rounding_type == Rounding.ROUNDINGUP:
#         print("CsvHandler rounding_process ROUNDINGUP　四捨五入")
#         if 0 < decimal_point_position:
#             self._csv_data[column_name] = self._csv_data[column_name].apply(
#                 lambda x: round(x, decimal_point_position)
#             )
#         else:
#             self._csv_data[column_name] = (
#                 self._csv_data[column_name].round().astype(int)
#             )
#     # 丸め処理
#     elif rounding_type == Rounding.TRUNCATE:
#         print("CsvHandler rounding_process TRUNCATE 少数切り捨て")
#         if 0 < decimal_point_position:
#             digit_adjustment_num = 10**decimal_point_position
#             self._csv_data[column_name] = self._csv_data[column_name].apply(
#                 lambda x: np.floor(x * digit_adjustment_num) / digit_adjustment_num
#             )
#         else:
#             self._csv_data[column_name] = self._csv_data[column_name].astype(int)
#     result = self._csv_data[column_name]
#     # print(result)

# 相関係数
# 1対1相関係数表示
#     corr_matrix = df.select_dtypes(include="number").corr()
#     corr_matrix[column_name]


# 1対多相関係数表示
#     result = df.select_dtypes(include="number").corr()
#     # グラフ表示
#     plt.figure(figsize=(8, 6))
#     sns.heatmap(result, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
#     plt.show()

# # 多重代入法
# # MICE
# def multiple_imputation_MICE(self, column_names):
#     csv_data_selected = self._csv_data[column_names]

#     mice_data = MICEData(csv_data_selected)
#     for i in range(10):
#         mice_data.update_all()
#     result = mice_data.data
#     print(result)

# # ランダムフォレスト
# def random_forest(self, target_column, column_array):
#     print("CsvHandler ModelProcesrandom_forest target_column:", target_column)
#     print("CsvHandler ModelProcesrandom_forest column_array:", column_array)
#     # age_df = self.data_instance.get_record(10)

#     # 推定に使用する項目を指定
#     target_df = self._csv_data[column_array]

#     # ラベル特徴量をワンホットエンコーディング
#     target_df = pd.get_dummies(target_df)

#     # 学習データとテストデータに分離し、numpyに変換
#     known_target_df = target_df[target_df[target_column].notnull()].values
#     unknown_target_df = target_df[target_df[target_column].isnull()].values

#     # 学習データをX, yに分離
#     X = known_target_df[:, 1:]
#     y = known_target_df[:, 0]

#     # ランダムフォレストで推定モデルを構築
#     rfr = RandomForestRegressor(random_state=0, n_estimators=100, n_jobs=-1)
#     rfr.fit(X, y)

#     # 推定モデルを使って、テストデータのAgeを予測し、補完
#     predictedAges = rfr.predict(unknown_target_df[:, 1::])
#     self._csv_data.loc[(self._csv_data[target_column].isnull()), target_column] = (
#         predictedAges
#     )
#     self.get_specification_record(target_column, 10)

#     # 年齢別生存曲線と死亡曲線
#     # facet = sns.FacetGrid(self._csv_data[0:890], hue="Survived",aspect=2)
#     # facet.map(sns.kdeplot,'Age',shade= True)
#     # facet.set(xlim=(0, self._csv_data.loc[0:890,'Age'].max()))
#     # facet.add_legend()
#     # plt.show()

# # 勾配ブースティング
# # point_column:補完対象カラム
# # column_array:補完対象外で利用するカラム
# def gradient_boosting(self, point_column, column_array):
#     print("CsvHandler gradient_boosting")
#     model = HistGradientBoostingRegressor()
#     df = self._csv_data
#     # 欠損していないデータを抽出（学習データ）
#     train_data = df[df[point_column].notnull()]
#     # print("gradient_boosting train_data=", train_data)

#     # 欠損データを抽出（テストデータ）
#     test_data = df[df[point_column].isnull()]
#     # print("gradient_boosting test_data=", test_data)
#     # 特徴量とターゲット変数を指定（ここでは'Age'がターゲット）
#     features = column_array
#     X_train = train_data[features]
#     # print("gradient_boosting X_train=", X_train)

#     y_train = train_data[point_column]
#     # print("gradient_boosting y_train=", y_train)

#     # モデルの学習
#     model.fit(X_train, y_train)

#     # 欠損値のあるデータ（test_data）から特徴量を取得
#     X_test = test_data[features]

#     # 欠損しているAgeを予測
#     predicted_ages = model.predict(X_test)

#     # 予測した値で欠損値を補完
#     df.loc[df[point_column].isnull(), point_column] = predicted_ages

#     # 結果を確認
#     # print(
#     #     "gradient_boosting 欠損値なし確認（0ならOK）",
#     #     df[point_column].isnull().sum(),
#     # )  # 欠損値が0になっているか確認

# # 外れ値チェック

# # 可視化
# # ヒストグラム
# df.hist(figsize=(10, 10), bins=30)
# plt.show()

# # ヒストグラム（指定）
# df[columns].hist(figsize=(10, 10), bins=30)
# plt.show()

# # ヒストグラム（カラム＋カラム内データ指定）
# def show_part_column_recrods_hist(self, column_name, records):
#     # ヒストグラムの重ね描き
#     plt.figure(figsize=(10, 10))
#     # Aカラムのヒストグラム
#     plt.hist(
#         self._csv_data[column_name],
#         bins=30,
#         alpha=0.5,
#         label="base",
#         color=Constant.BASE_COLOR,
#     )
#     plt.hist(
#         self._csv_data[column_name].loc[records],
#         bins=30,
#         alpha=0.5,
#         label=column_name,
#         color="orange",
#     )
#     plt.legend()
#     # グラフを表示
#     plt.show()

# # 異なるモデルを比較するヒストグラム
# def show_compare_column_recrods_hist(
#     self, column_name, models_results01, models_results02, records
# ):
#     # ヒストグラムの重ね描き
#     plt.figure(figsize=(10, 10))
#     # 基準のヒストグラム
#     plt.hist(
#         self._csv_data[column_name],
#         bins=30,
#         alpha=0.5,
#         label="base",
#         color=Constant.BASE_COLOR,
#     )

#     plt.hist(
#         models_results01[column_name].loc[records],
#         bins=30,
#         alpha=0.5,
#         label=column_name,
#         color=Constant.COLORS[0],
#     )

#     plt.hist(
#         models_results02[column_name].loc[records],
#         bins=30,
#         alpha=0.5,
#         label=column_name,
#         color=Constant.COLORS[1],
#     )

#     # for index, model in models_results:
#     #     plt.hist(
#     #         model[column_name].loc[records],
#     #         bins=30,
#     #         alpha=0.5,
#     #         label=column_name,
#     #         color=Constant.COLORS[index],
#     #     )
#     plt.legend()
#     # グラフを表示
#     plt.show()

# カーネル密度推定（KDE）
# sns.kdeplot(df, shade=True)


# ペアプロット
# sns.pairplot(df, diag_kind="kde")
# plt.show()

# ボックスプロット（箱ひげ図）
# plt.figure(figsize=(8, 6))
# plt.boxplot([df[col] for col in column_names], labels=column_names)
# plt.title("Box Plot")
# plt.ylabel("Values")
# plt.show()