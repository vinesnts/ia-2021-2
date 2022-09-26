import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SL = "sepal length in cm"
SW = "sepal width in cm"
PL = "petal length in cm"
PW = "petal width in cm"

iris_cols = [SL, SW, PL, PW, "classe"]
data = pd.read_csv('./atividade5/iris.data', header=None, names=iris_cols)

X_train, X_test, y_train, y_test = train_test_split(data[iris_cols[:-1]], data[iris_cols[-1]], test_size=0.5)

model = KMeans(n_clusters=3)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

acertos = accuracy_score(y_test, y_pred)
print(f"Taxa de acertos: {acertos*100:.0f}%")

