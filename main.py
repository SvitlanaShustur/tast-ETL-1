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
#### Перевіряємо записи у стовпці "email", "web", "phone1", "phone2"
# print(df['first_name'].head(5))
# print(df['last_name'].head(5))
# print(df['company_name'].head(5))
# print(df['address'].head(5))
# print(df['city'].head(5))
# print(df['county'].head(5))
# print(df['postal'].head(5))
# print(df['phone1'].head(5))
# print(df['phone2'].head(5))
# print(df['web'].head(5))
# # df = df.drop("phone2", axis=1) # видаляємо стовпець "phone2"
# df['email'] = df['email'].str.lower()
# df['web'] = df['web'].str.lower()

df['phone1_1'] = df['phone1'].copy() # створюємо копію стовпця "phone1"
df['phone1_1'] = df['phone1_1'].astype(str).str.replace('-', '', regex=True)    # видаляємо дефіси
df['phone1_2'] = df['phone1_1'].copy() # створюємо копію стовпця "phone1_1"
df['phone1_2'] = df['phone1_1'].str[1:] # видаляємо перший символ (0)
# print(df['phone1_2'].head(5))

df['telephon'] = '+44 ' + df['phone1_2'] # додаємо код країни +44
df['telephon'] = (
    df['telephon'].str[:6] + ' ' +  # Беремо перші 6 символів (+441944) і додаємо пробіл
    df['telephon'].str[6:10] + " " + # Додаємо наступні 4 символи (7700) і додаємо пробіл
    df['telephon'].str[10:14]               # Додаємо останні 4 символи (1234)
)  # +44 770
print(df['telephon'].head(5))