# -*- coding: utf-8 -*-
"""Randomforest.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zLGhMjCFY5On5GvfVceoONiGTZMUz9O3
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Excel dosyasını oku
df = pd.read_excel('/content/Ogrenci_Performans.xlsx')

# Özel ders alan ve almayan öğrencileri gruplayalım
df['Ozel Ders'] = df['Ozel Ders'].map({'Var': 1, 'Yok': 0})

# 1. Özel Ders Almanın Başarıya Etkisi
X = df[['Ozel Ders']]
y = df[['Matematik', 'Okuma', 'Yazma']].mean(axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)
effect_ozel_ders = model.feature_importances_[0]

print("Özel dersin başarıya etkisi: {:.2f}".format(effect_ozel_ders))
print("Özel ders, genel başarı notu üzerinde önemli bir etkiye sahiptir. Random Forest Regresyon modeline göre, özel ders almanın öğrencilerin matematik, okuma ve yazma performansını doğrudan etkilediği söylenebilir..")

# 2. Hangi faktörlerin başarıya Etkisi Yoktur?
#Katsayı değeri 0.05 veya daha düşük olan faktörler, başarı üzerinde önemsiz veya etkisiz olduğunu düşünebileceğimiz faktörlerdir.
df = pd.get_dummies(df, drop_first=True)
A = df.drop(columns=['Matematik', 'Okuma', 'Yazma'])
B = df[['Matematik', 'Okuma', 'Yazma']].mean(axis=1)

model = RandomForestRegressor()
model.fit(A, B)

coefficients = pd.DataFrame(model.feature_importances_, A.columns, columns=['Katsayı'])
print(coefficients)
print("Randomforest modeline göre incelediğimiz zaman okul Yemekhanesi'nin varlığı veya yokluğunun öğrencilerin matematik, okuma ve yazma başarısı üzerinde önemli bir etkisi olmadığı sonucuna varabiliriz. ")

# 3. Hangi faktörler başarıyı en çok etkilemektedir?
X = df.drop(["Okuma", "Yazma", "Matematik"], axis=1)
y = df[["Okuma", "Yazma", "Matematik"]].mean(axis=1)

X = pd.get_dummies(X, drop_first=True)

model = RandomForestRegressor()
model.fit(X, y)

faktorler = dict(zip(X.columns, model.feature_importances_))
en_etkili_faktorler = sorted(faktorler.items(), key=lambda x: abs(x[1]), reverse=True)

print("Başarıyı En Çok Etkileyen Faktörler ve Katsayıları:\n")
for faktor, etki in en_etkili_faktorler:
    print(faktor, ":", etki)
print("\n")

# 4. Okuma becerisinin yazma ve matematik üzerindeki etkisi nedir?
A = df[["Okuma"]].values
B_yazma = df[["Yazma"]].values
B_matematik = df[["Matematik"]].values

A_train, A_test, B_yazma_train, B_yazma_test = train_test_split(A, B_yazma, test_size=0.2, random_state=42)
A_train, A_test, B_matematik_train, B_matematik_test = train_test_split(A, B_matematik, test_size=0.2, random_state=42)

model_yazma = RandomForestRegressor()
model_yazma.fit(A_train, B_yazma_train.ravel())

model_matematik = RandomForestRegressor()
model_matematik.fit(A_train, B_matematik_train.ravel())

yazma_pred = model_yazma.predict(A_test)
matematik_pred = model_matematik.predict(A_test)

okuma_yazma_etkisi = model_yazma.feature_importances_[0]
okuma_matematik_etkisi = model_matematik.feature_importances_[0]

okuma_yazma_aciklama = "Okuma becerisinin Yazma üzerindeki etkisi: {:.2f}".format(okuma_yazma_etkisi)
okuma_matematik_aciklama = "Okuma becerisinin Matematik üzerindeki etkisi: {:.2f}".format(okuma_matematik_etkisi)

print(okuma_yazma_aciklama)
print(okuma_matematik_aciklama)
print("okuma becerisinin hem yazma hem de matematik becerileri üzerinde kuvvetli bir etkiye sahip olduğunu gösterir. Okuma becerisi yüksek olan öğrencilerin hem yazma hem de matematik alanında daha başarılı oldukları düşünülebilir.")
