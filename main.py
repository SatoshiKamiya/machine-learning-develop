import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style='darkgrid', font_scale=1.6)
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, f1_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import os
os.environ["WANDB_DISABLED"] = "true"

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
import datasets
from datasets import load_dataset
def main():
    print("main処理開始")
    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("data/test.csv")
    sub = pd.read_csv("data/sample_submission.csv")

    print("トレーニング　行列数")
    print(train.shape)
    print("test　行列数")
    print(test.shape)
    print("sub　行列数")
    print(sub.shape)
    print("トレーニング　head")
    print(train.head(5))

    # 棒グラフ
    plt.figure(figsize=(10,4))
    sns.countplot(data=train, x="Rating")
    plt.title("Target distribution")
    plt.show()

    # Map labels
    train["Rating"] = train["Rating"] - 1 #rating=1~5 →　0~4へ変更

    # ターゲット（rating）を取り除いたトレーニングデータ（8:2）
    X_train, X_valid, _, _ = train_test_split(train, train["Rating"], test_size=0.2, shuffle=True, random_state=0)
    
    # カラム名を変更　Review → text、Rating → label
    # 変更したデータを「new_train.csv」に保存する
    X_train[["Review","Rating"]].rename(columns={"Review":"text", "Rating":"label"}).to_csv("new_train.csv", index=False)
    



   

if __name__ == "__main__":
    main()
