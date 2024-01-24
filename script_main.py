
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import os
import urllib.parse
import joblib

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)  # making full path to file
    with open(filepath, 'r',encoding="utf8") as f:
        data = f.readlines()
    data = list(set(data))  # removing duplicate lines
    result = []
    for d in data:
        d = str(urllib.parse.unquote(d))  # converting URL encoded data to simple string
        result.append(d)
    return result


badQueries = loadFile('badqueries.txt')
goodQueries = loadFile('goodqueries.txt')

badQueries = list(set(badQueries))
goodQueries = list(set(goodQueries))

allQueries = badQueries + goodQueries
yBad = [1 for i in range(0, len(badQueries))]
yGood = [0 for i in range(0, len(goodQueries))]
y = yBad + yGood
queries = allQueries

vectorizer = TfidfVectorizer(min_df=0.0, analyzer="char", sublinear_tf=True, ngram_range=(1, 3))
X = vectorizer.fit_transform(queries)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

badCount = len(badQueries)
goodCount = len(goodQueries)

rf = RandomForestClassifier(class_weight={1: 2 * goodCount / badCount, 0: 1.0}, n_estimators=100)
rf.fit(X_train, y_train)


joblib.dump(rf, 'random_forest_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

predicted = rf.predict(X_test)

fpr, tpr, _ = metrics.roc_curve(y_test, (rf.predict_proba(X_test)[:, 1]))
auc = metrics.auc(fpr, tpr)

print("Bad samples: %d" % badCount)
print("Good samples: %d" % goodCount)
print("Baseline Constant negative: %.6f" % (goodCount / (goodCount + badCount)))
print("------------")
print("Accuracy: %f" % rf.score(X_test, y_test))  # checking the accuracy
print("Precision: %f" % metrics.precision_score(y_test, predicted))
print("Recall: %f" % metrics.recall_score(y_test, predicted))
print("F1-Score: %f" % metrics.f1_score(y_test, predicted))
print("AUC: %f" % auc)
