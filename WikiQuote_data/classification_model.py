import numpy as np
import pandas as pd
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multioutput import MultiOutputClassifier

df = pd.read_table("data/enwikiquote-20170206-cirrussearch-text-categories_train.tsv",header=None,names=['text','categories'])
df = df.dropna()
df['categories'] = df['categories'].dropna().apply(lambda x: x.split(";"))
s = df['categories'].apply(pd.Series).unstack().dropna()

# top 100 categories
top_categories = s.value_counts()[:100].index.values
df['categories'] = df['categories'].apply(lambda x: [c for c in x if c in top_categories])

clf = Pipeline([
	('vect', CountVectorizer(ngram_range=(1,2),min_df=5, max_df=0.9, max_features=40000)),
	('tfidf', TfidfTransformer()),
	('clf', MultiOutputClassifier(LinearSVC(tol=1e-3), n_jobs=-1))
])
lbl = MultiLabelBinarizer().fit(df['categories'])

clf.fit(df['text'], lbl.fit_transform(df['categories']))

df['pred'] = [lbl.classes_[np.where(res)[0]] for res in clf.predict(df['text'])]

joblib.dump(clf, "model/clf.jbl")
joblib.dump(lbl, "model/lbl.jbl")

df.to_csv("out.tsv", sep='\t', index=False)
