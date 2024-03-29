from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from logisticRegressionClassifier import LogisticRegression
import numpy as np
import pandas as pd


df= pd.read_csv('breast-cancer-wisconsin.csv', header=None)

X = df.loc[:, 1:10] # 699 rows × 10 columns
y = df.loc[:, 10]   #class labels: 2 = benign, 4 = malignant 699x2

le = LabelEncoder() #positive class = 1 (benign), negative class = 0 (malignant) ac tinh
y = le.fit_transform(y)   #đã chuyển thành mảng 699 phantu

#Replace missing feature values with mean feature value
X = X.replace('?', np.nan)
imr = SimpleImputer(missing_values= np.NAN, strategy= 'mean', fill_value=None, verbose=0, copy=True)
imr = imr.fit(X)
X_imputed = imr.transform(X.values) #mảng 699 hang, 10 cot

#Split data into training (70%) and testing (30%) sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size = 0.3, random_state = 1)

#Z-score normalization, New value = (x – μ) / σ, giam su anh huong cua outlier
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Principle component analysis (dimensionality reduction)
pca = PCA(n_components = 2)
X_train_pca = pca.fit_transform(X_train) #699 hang, 2 cot
X_test_pca = pca.transform(X_test)

#Training logistic regression classifier with L2 penalty
LR = LogisticRegression(learningRate = 0.01, numIterations = 20, penalty = 'L2', C = 0.01)
LR.train(X_train_pca, y_train, tol = 10 ** -3)


#Testing fitted model on test data with cutoff probability 50%
predictions, probs = LR.predict(X_test_pca, 0.5)
performance = LR.performanceEval(predictions, y_test)
LR.plotDecisionRegions(X_test_pca, y_test)
LR.predictionPlot(X_test_pca, y_test)

#Print out performance values
for key, value in performance.items():
    print('%s : %.4f' % (key, value))


