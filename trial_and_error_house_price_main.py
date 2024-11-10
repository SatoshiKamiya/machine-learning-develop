import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.experimental import enable_iterative_imputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


def main():
    print("main処理開始")
    # 1つ目のモデル用
    train_df = pd.read_csv("data/house_prices/train.csv")
    test_df = pd.read_csv("data/house_prices/test.csv")
    total_df = pd.concat([train_df, test_df], ignore_index=True, sort=False)
    # print("tranigデータ数：", train_df.shape[0]) # 1460
    # print("testデータ数：", test_df.shape[0]) # 1459

    # 列数50まで表示
    pd.set_option("display.max_columns", 50)

    # ---------------------------カラム相関チェック後抽出後データ--------------------------------
    # 数値のみ
    num_total_df = total_df[
        [
            "SalePrice",  # 目的変数
            "MasVnrArea",  # 欠損値補完対象
            "GarageYrBlt",  # 欠損値補完対象
            "OverallQual",
            "YearBuilt",
            "YearRemodAdd",
            "BsmtFinSF1",
            "TotalBsmtSF",
            "1stFlrSF",
            "2ndFlrSF",
            "GrLivArea",
            "FullBath",
            "TotRmsAbvGrd",
            "Fireplaces",
            "GarageCars",
            "GarageArea",
            "WoodDeckSF",
            "OpenPorchSF",
        ]
    ]
    # 相関係数チェック
    # num_total_df_corr = num_total_df.corr()
    # print("num_total_df　補完前相関チェック")
    # print(num_total_df_corr)

    # 文字列は別途用意　まずは数値のみデータの外れ値と欠損値補完する

    # -----------------------------------------------------------------------------------------

    # レコード数 最大数2919
    # print("records count=", total_df.shape[0])
    # 型＆nullチェック
    print("型＆nullチェック")
    print(total_df.info())
    # データ一部表示
    print("head")
    print(total_df.head())

    # ---------------------------欠損値チェックとランダムフォレストに魚る補完--------------------------------
    # 欠損値のある行番号を取得
    MasVnrArea_drop_records = total_df[total_df["MasVnrArea"].isnull()].index

    print("MasVnrArea　欠損レコード数")
    print(MasVnrArea_drop_records)

    # MasVnrAreaを補完するためのカラム
    complement_MasVnrArea_df = total_df[
        [
            "MasVnrArea",
            "OverallQual",
            "TotalBsmtSF",
            "1stFlrSF",
            "GrLivArea",
            "GarageCars",
            "GarageArea",
        ]
    ]

    # 相関係数チェック
    MasVnrArea_df_corr = complement_MasVnrArea_df.corr()
    print("MasVnrArea　補完前相関チェック")
    print(MasVnrArea_df_corr)

    # ランダムフォレストによる補完 MasVnrArea
    print("MasVnrArea ランダムフォレストによる補完開始")
    model = IterativeImputer(
        estimator=RandomForestRegressor(), max_iter=10, random_state=0
    )
    data_imputed = model.fit_transform(complement_MasVnrArea_df)  # 必要なカラムを指定
    # total_df = pd.DataFrame(data_imputed, columns=complement_MasVnrArea_df.columns)
    num_total_df["MasVnrArea"] = pd.DataFrame(
        data_imputed, columns=complement_MasVnrArea_df.columns
    )["MasVnrArea"]
    print("欠損値補完確認")
    print(num_total_df["MasVnrArea"].loc[MasVnrArea_drop_records])

    # GarageYrBltを補完するためのカラム
    complement_GarageYrBlt_df = total_df[
        [
            "GarageYrBlt",
            "OverallQual",
            "YearBuilt",
            "YearRemodAdd",
            "FullBath",
            "GarageCars",
            "GarageArea",
        ]
    ]
    complement_GarageYrBlt_df_corr = complement_GarageYrBlt_df.corr()
    print("GarageYrBlt　相対係数チェック")
    print(complement_GarageYrBlt_df_corr)
    print("complement_GarageYrBlt_df　値チェック")
    print(complement_GarageYrBlt_df.describe())

    GarageYrBlt_drop_records = total_df[total_df["GarageYrBlt"].isnull()].index
    print("GarageYrBlt　欠損値レコード一覧")
    print(GarageYrBlt_drop_records)

    # ランダムフォレストによる補完 GarageYrBlt
    print("GarageYrBlt ランダムフォレストによる補完開始")

    model = IterativeImputer(
        estimator=RandomForestRegressor(), max_iter=10, random_state=0
    )

    data_imputed = model.fit_transform(complement_GarageYrBlt_df)  # 必要なカラムを指定
    total_df = pd.DataFrame(data_imputed, columns=complement_GarageYrBlt_df.columns)
    num_total_df["GarageYrBlt"] = pd.DataFrame(
        data_imputed, columns=complement_GarageYrBlt_df.columns
    )["GarageYrBlt"]

    print("欠損値補完確認")
    print(num_total_df["GarageYrBlt"].loc[GarageYrBlt_drop_records])

    print("型＆nullチェック　GarageYrBlt欠損値補完後")
    print(num_total_df.info())

    # 最後に欠損値があるすべてのカラムに対して中央値で補完
    columns_to_impute = [
        "BsmtFinSF1",
        "TotalBsmtSF",
        "GarageCars",
        "GarageArea",
    ]  # 指定して補完
    imputer = SimpleImputer(strategy="median")
    num_total_df[columns_to_impute] = imputer.fit_transform(
        num_total_df[columns_to_impute]
    )

    print("型＆nullチェック　学習前最終確認")
    # 全データ正規化
    standardScaler = StandardScaler()
    data_normalized = standardScaler.fit_transform(num_total_df)
    num_total_df = pd.DataFrame(data_normalized, columns=num_total_df.columns)

    print(num_total_df.info())
    print(num_total_df.describe())

    # データをカラムを変更し、レコードを最初の状態に戻す
    # トレーニングデータ
    num_total_df_traning = num_total_df[num_total_df["SalePrice"].notnull()]
    num_total_df_predict = num_total_df[num_total_df["SalePrice"].isnull()].drop(
        "SalePrice", axis=1
    )

    print("tranigデータ数：", num_total_df_traning.shape[0])  # 1460
    print("testデータ数：", num_total_df_predict.shape[0])  # 1459

    # 説明変数・目的変数
    X = num_total_df_traning.drop("SalePrice", axis=1)  # 説明変数
    y = num_total_df_traning["SalePrice"]  # 目的変数
    # データの前処理（例：欠損値補完やエンコーディング）
    # X = pd.get_dummies(X, drop_first=True)  # ワンホットエンコーディングなどの前処理を適用

    # 訓練データとテストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    # print("型＆nullチェック　X_train確認")
    # print(X_train.info())
    # print(X_train.describe())
    # print("型＆nullチェック y_train確認")
    # print(y_train.info())
    # print(y_train.describe())

    # 学習
    # XGBoostモデルの定義と学習
    model = xgb.XGBRegressor(
        objective="reg:squarederror",  # 回帰用の目的関数
        n_estimators=100,  # 木の数（ブースティングの反復回数）
        learning_rate=0.1,  # 学習率
        max_depth=5,  # 木の深さ
        random_state=42,
    )
    model.fit(X_train, y_train)

    # テストデータで予測
    y_pred = model.predict(X_test)

    # 予測結果
    # plt.figure(figsize=(8, 6))
    # plt.scatter(y_test, y_pred, alpha=0.5, color="b")
    # plt.plot(
    #     [y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--"
    # )  # 対角線
    # plt.xlabel("Actual values")
    # plt.ylabel("Predicted values")
    # plt.title("Actual vs Predicted values")
    # plt.show()

    # 評価指標（RMSE）を計算
    # rmse = mean_squared_error(y_test, y_pred, squared=False)
    # print(f"RMSE: {rmse}")

    final_predict_result = model.predict(num_total_df_predict)
    num_total_df_predict["SalePrice"] = final_predict_result

    final_predict_result_original_inv = standardScaler.inverse_transform(
        num_total_df_predict
    )
    final_predict_result_original = pd.DataFrame(
        final_predict_result_original_inv, columns=num_total_df.columns
    )
    # 丸め処理
    final_predict_result_original["SalePrice"] = final_predict_result_original[
        "SalePrice"
    ].astype(int)

    # 提出準備
    submission = pd.DataFrame(
        {"Id": test_df["Id"], "SalePrice": final_predict_result_original["SalePrice"]}
    )
    print("提出前最終チェック")
    print(submission.info())
    print(submission.describe())
    print(submission.head(1500))
    submission.to_csv("submission.csv", index=False)


# -----------------------------------------------------------------------------------------
# # 相関係数
# numeric_df = train_df.select_dtypes(include=[float, int])
# # カラムチェック
# print("カラムの種類", numeric_df.columns)

# salePrices check
# print("セール価格の統計値")
# print(train_df["SalePrice"].describe())

# ---------------------------One-Hot Encoding相関関係チェック--------------------------------
# print("Neighborhood")
# print(train_df["Neighborhood"].value_counts())
# print("ExterQual")
# print(train_df["ExterQual"].value_counts())
# print("BsmtQual")
# print(train_df["BsmtQual"].value_counts())
# print("KitchenQual")
# print(train_df["KitchenQual"].value_counts())
# print("GarageFinish")
# print(train_df["GarageFinish"].value_counts())

# train_df = train_df[["SalePrice", "ExterQual", "BsmtQual", "BsmtQual"]]

# One-Hot Encodingを適用
# df_encoded = pd.get_dummies(train_df, columns=["ExterQual"]).astype(int)
# df_encoded = pd.get_dummies(train_df).astype(int)

# print("中間チェック")
# print(df_encoded)
# 相関を計算
# bsmtqual_columns = [
#     col for col in df_encoded.columns if col.startswith("ExterQual" + "_")
# ]
# correlation_matrix = df_encoded.corr()["SalePrice"][bsmtqual_columns]

# print("SalePrice vs GarageFinish")
# print(correlation_matrix)

# ---------------------------文字列データ選定--------------------------------
# cor_str_train_df = train_df[
#     [
#         "Neighborhood",
#         "ExterQual",
#         "BsmtQual",
#         "KitchenQual",
#         "GarageFinish",
#     ]
# ]
# print("info=", cor_str_train_df.info())
# `---------------------------文字列内の相関選定--------------------------------
# cor_str_train_df_01 = train_df[
#     [
#         "SalePrice",
#         "Street",
#         "Alley",
#         "LotShape",
#         "LandContour",
#         "Utilities",
#         "LotConfig",
#         "LandSlope",
#         "Neighborhood",
#         "Condition1",
#         "Condition2",
#         "BldgType",
#         "HouseStyle",
#     ]
# ]

# pd.set_option("display.max_rows", 500)
# print("head")
# print(cor_str_train_df_01.head(300))

# `---------------------------相関係数による相関選定----------------------------
# cor_train_df_01 = train_df[
#     [
#         "SalePrice",
#         "LotFrontage",
#         "OverallQual",
#         "YearBuilt",
#         "YearRemodAdd",
#         "MasVnrArea",
#         "BsmtFinSF1",
#         "TotalBsmtSF",
#         "1stFlrSF",
#         "2ndFlrSF",
#         "GrLivArea",
#         "FullBath",
#     ]
# ]

# cor_train_df_02 = train_df[
#     [
#         "SalePrice",
#         "TotRmsAbvGrd",
#         "Fireplaces",
#         "GarageYrBlt",
#         "GarageCars",
#         "GarageArea",
#         "WoodDeckSF",
#         "OpenPorchSF",
#     ]
# ]

# cor_train_df_03 = train_df[
#     [
#         "SalePrice",
#         "BedroomAbvGr",
#         "KitchenAbvGr",
#     ]
# ]

# cor = cor_train_df_03.corr()
# sns.heatmap(
#     cor,
#     cmap=sns.color_palette("coolwarm", 10),
#     annot=True,
#     fmt=".2f",
#     vmin=-1,
#     vmax=1,
# )
# plt.show()
# print(correlation_matrix)


if __name__ == "__main__":
    main()
