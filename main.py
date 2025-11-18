import csv
import pandas as pd


### **1. Імпорт та первинне дослідження**

url = 'https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv' # визначаємо дані
df = pd.read_csv(url) # завантажуємо дані у DataFrame
# print(df) # виводимо дані на екран
# df.info() # отримуємо інформацію про DataFrame
# df.describe() # отримуємо статистичний опис даних
# print("----")
# print(df.isna().sum()) # перевіряємо на наявність пропущених значень
# print(df.duplicated().sum()) # перевіряємо на наявність дублікатів


### **2. Очищення даних**
df_1 = df['phone1']
# df = df.drop("phone2", axis=1) # видаляємо стовпець "phone2"
df.info()   # перевіряємо інформацію про DataFrame після видалення стовпця
df['email'] = df['email'].str.lower()
df['web'] = df['web'].str.lower()
df['phone1'] = df['phone1'].str.strip()
df['phone2'] = df['phone2'].str.strip()
print(df_1)