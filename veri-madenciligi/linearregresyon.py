# -*- coding: utf-8 -*-
"""LinearRegresyon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mwEVbHuxCvSkyVJwu4KjSFksup3SyQ_A
"""

import pandas as pd
import statsmodels.api as sm

# Excel dosyasını oku
df = pd.read_excel('/content/Ogrenci_Performans.xlsx')

# Özel ders alan ve almayan öğrencileri gruplayalım
df['Ozel Ders'] = df['Ozel Ders'].map({'Var': 1, 'Yok': 0})

X = df[['Ozel Ders']]
y = df[['Matematik', 'Okuma', 'Yazma']].mean(axis=1) #Bağımlı ve bağımsız değişkenleri belirleyelim.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

#1.Özel Ders ALmanın Başarıya Etkisi?
effect_ozel_ders = model.coef_[0]
print("Özel dersin başarıya etkisi:", effect_ozel_ders)

#2.Hangi faktörlerin başarıya Etkisi Yoktur?
# Doğrusal regresyon modelini kullanarak bu analizi yapmak için, öncelikle kategorik değişkenlerinizi düzgün bir formatta olmalıdır. Bu, genellikle "one-hot encoding" denilen bir işlem gerektirir.
df = pd.get_dummies(df, drop_first=True)
A = df.drop(columns=['Matematik', 'Okuma', 'Yazma'])
B = df[['Matematik', 'Okuma', 'Yazma']].mean(axis=1)
 # Artık tüm özelliklerin üzerinde bir regresyon modeli oluşturabiliriz. Bu modelde, bağımsız değişkenler (X) tüm özellikler olacak, bağımlı değişken (y) ise genel başarı notu olacaktır.
model = LinearRegression()
model.fit(A, B)

coefficients = pd.DataFrame(model.coef_, A.columns, columns=['Katsayı'])
# Modeli oluşturduk, eğittik ve katsayıları aldık.
print(coefficients)
print("Hepsinin başarıya etkisi vardır ancak pozitif bir katsayı, o özelliğin genel başarı puanını artırma eğiliminde olduğunu, negatif bir katsayı ise genel başarı puanını azaltma eğiliminde olduğunu gösterir. Yani EBEVEYN EĞİTİM SEVİYESİ LİSE VE ÖNLİSANS olanların, okul yemekhanesi olmayanların ve özel ders almayanların başarıya etkisi negatiftir.")

#3.Hangi faktörler başarıyı en çok etkilemektedir?
# Bağımsız değişkenler (X) ve hedef değişken (y) olarak verileri ayıralım.
X = df.drop(["Okuma", "Yazma", "Matematik"], axis=1)
y = df[["Okuma", "Yazma", "Matematik"]].mean(axis=1)  # Okuma, Yazma ve Matematik sütunlarının ortalamasını alarak başarıyı temsil eden y değişkenini oluşturduk.

# Kategorik sütunları dönüştürmek için One-Hot Encoding uyguladık.
X = pd.get_dummies(X, drop_first=True)

model = LinearRegression()
model.fit(X, y)

# Katsayıları ve faktörleri eşleştirdim.
faktorler = dict(zip(X.columns, model.coef_))

# Faktörleri etki sırasına göre sıraladım.
en_etkili_faktorler = sorted(faktorler.items(), key=lambda x: abs(x[1]), reverse=True)

# En çok etkileyen faktörleri yazdıralım.
print("Başarıyı En Çok Etkileyen Faktörler ve Katsayıları:\n")
for faktor, etki in en_etkili_faktorler:
    print(faktor, ":", etki)
print("\n")

#4.Okuma becerisinin yazma ve matematik üzerindeki etkisi nedir?
print("------4.soru ----------")
A = df[["Okuma"]]
B = df[["Yazma", "Matematik"]]

# Eğitim ve test verilerini ayırdık.
A_train, A_test, B_train, B_test = train_test_split(A, B, test_size=0.2, random_state=42)

# Lineer regresyon modelini oluşturun ve eğittik.
model = LinearRegression()
model.fit(A_train, B_train)

# Test verilerini kullanarak tahmin yaptık.
B_pred = model.predict(A_test)

etki = model.coef_
okuma_yazma_etkisi = etki[0]
okuma_matematik_etkisi = etki[1]

okuma_yazma_aciklama = "Okuma becerisinin Yazma üzerindeki etkisi: {:.2f}".format(okuma_yazma_etkisi[0])
okuma_matematik_aciklama = "Okuma becerisinin Matematik üzerindeki etkisi: {:.2f}".format(okuma_matematik_etkisi[0])

print(okuma_yazma_aciklama)
print("Verilerimize göre, öğrencilerin okuma becerisi yazma becerisi üzerinde önemli bir etkiye sahiptir. Okuma becerisi ile yazma becerisi arasında pozitif bir ilişki bulunmaktadır. Yani, okuma becerisi arttıkça, yazma becerisi de artmaktadır. Bu analizde elde ettiğimiz sonuçlara göre, okuma becerisinin yazma becerisi üzerindeki etkisi 1.00'dir. Bu, okuma becerisinin yazma becerisi üzerinde oldukça güçlü bir etkisi olduğunu göstermektedir.")

print(okuma_matematik_aciklama)
print("Bunun yanı sıra, okuma becerisinin matematik becerisi üzerinde de bir etkisi olduğu görülmektedir. Elde ettiğimiz sonuçlara göre, okuma becerisinin matematik becerisi üzerindeki etkisi 0.85'tir. Bu da okuma becerisinin matematik becerisini olumlu yönde etkilediğini göstermektedir. Ancak, yazma becerisi üzerindeki etkisine kıyasla matematik becerisi üzerindeki etkisi biraz daha düşüktür.")

"""# Yeni Bölüm"""