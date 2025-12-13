import csv
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)  # показувати всі стовпці
# pd.set_option('display.max_columns', 50)  # максимальна кількість стовпців для відображення
pd.set_option('display.width', 120)  # ширина виводу. 120 символів можуть бути виведені в одному рядку. можуть редакуватися


### **1. Імпорт та первинне дослідження**

url = 'https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv' # визначаємо дані
df_origin = pd.read_csv(url) # завантажуємо дані у DataFrame
df = df_origin.copy()
COLUMNS_TO_DROP = []
# print("\n---  head ---")
print(df.head(5)) # виводимо перші 5 записів на екран

print("\n---  info ---")
df.info() # отримуємо інформацію про DataFrame

print("\n---  describe ---")
df.describe() # отримуємо статистичний опис даних

print("\n---  describe for str ---")
print(df.describe(include=[object]).T) # 

print("\n---  isna / null  ---")
print(df.isna().sum().sort_values(ascending=False).head(20)) # перевіряємо на наявність пропущених значень. Сортуємо за спаданням та виводимо перші 20

print("\n---  duplicated ---")
print(df.duplicated().sum()) # перевіряємо на наявність дублікатів

print("\n---  List colums 1 ---") # виводимо список стовпців
list_col = df.columns # зберігаємо список стовпців у змінну
print(list(list_col)) # виводимо список стовпців у вигляді списку

print("\n---  List colums 2 ---") # виводимо список стовпців з індексами
for i, col in enumerate(df.columns): # виводимо індекс та назву кожного стовпця
    print(f"{i:02d}. {col}") # виводимо індекс та назву стовпця з провідними нулями



### **2. Очищення даних**

#1. Видаляємо непотрібні стовпці. Універсальний варіант
df = df_origin.copy() # створюємо копію DataFrame для збереження оригінальних даних
print(df)
if COLUMNS_TO_DROP: # якщо є стовпці для видалення
    print("\n--- delete columns in lisr ---") # виводимо повідомлення
    df = df.drop(colums=[col for col in COLUMNS_TO_DROP if df in df.columns], errors="ignore") # видаляємо стовпці зі списку COLUMNS_TO_DROP, якщо вони є у DataFrame

else:
    print("\n--- no columns to delete ---") # виводимо повідомлення, якщо немає стовпців для видалення


# Функція для стандартизації тексту (видалення зайвих пробілів, приведення до рядка)
def standardize_text(s): # функція для стандартизації тексту
    if pd.isna(s): # перевіряємо на пропущене значення
        return np.nan # повертаємо NaN, якщо значення пропущене
    
    if not isinstance(s, str): # перевіряємо, чи є значення рядком/-- isinstance це вбудована функція в мові програмування Python, яка перевіряє, чи є об'єкт екземпляром певного класу або одного з його підкласів
        s = str(s) # перетворюємо значення на рядок, якщо це не так

    s = s.strip() # видаляємо пробіли на початку та в кінці рядка
    s = ' '.join(s.split()) # видаляємо зайві пробіли між словами

    return s # повертаємо стандартизований / очищений рядок

# Привести `email` та `web` до нижнього регістру.
# Ідентифікуємо можливі стовпці з email, web, phone, fax
possible_email_cols = [c for c in df.columns if "email" in c.lower()] # знаходимо всі стовпці, які містять "email" у назві
possible_web_cols = [c for c in df.columns if ("web" in c.lower() or "website" in c.lower() or "url" in c.lower())] # знаходимо всі стовпці, які містять "web", "website" або "url" у назві
possible_phone_cols = [c for c in df.columns if ("phone" in c.lower() or "telephon" in c.lower() or "tel" in c.lower() or "mobile" in c.lower())] # знаходимо всі стовпці, які містять "phone", "tel" або "mobile" у назві
possible_fax_cols = [c for c in df.columns if ("fax" in c.lower())] # знаходимо всі стовпці, які містять "fax" у назві

# Привести `email` та `web` до нижнього регістру.
# Застосовуємо функцію стандартизації тексту до всіх стовпців типу object (рядок)
for col in df.select_dtypes(include=['object']).columns: # ітеруємося по всіх стовпцях типу object
    df[col] = df[col].apply(standardize_text) # застосовуємо функцію стандартизації тексту до кожного стовпця

for col in possible_email_cols: # ітеруємося по можливих стовпцях з email
    df[col] = df[col].str.lower() # перетворюємо всі символи на малі літери

for col in possible_web_cols: # ітеруємося по можливих стовпцях з web
    df[col] = df[col].str.lower() # перетворюємо всі символи на малі літери


def clean_phone(x):
    if pd.isna(x): # перевіряємо на пропущене значення
        return np.nan # повертаємо NaN, якщо значення пропущенеs
    s = str(x)
    
    plus = "+" if s.startswith("+") else "" # якщо рядок починається з "+", зберігаємо знак "+", інакше залишаємо порожній рядоr
    
    digits = "".join(ch for ch in s if ch.isdigit())
    if digits == "":
        return np.nan
    return plus + digits

for col in possible_phone_cols + possible_fax_cols:
    df[col] = df[col].apply(clean_phone)


def title_if_str(s):
    if pd.isna(s):
        return np.nan
    return str(s).title()

city_cols = [c for c in df.columns if c.lower() in ("city", "city_name", "town")]

address_cols = [c for c in df.columns if c.lower() in ("address")]

name_cols = [c for c in df.columns if c.lower() in ("name", "first_name", "second_name", "last_name", "company_name")]

name_title = city_cols + address_cols + name_cols

if name_title:
    for col in name_title:
        df[col] = df[col].apply(title_if_str)
    print("\n--- name of title ---")
else:
    print('\n--- haven `t name ---')


### **3. Створення нових колонок (Feature Engineering)**
df["full_name"] = df.first_name + " " + df.last_name

df["city_length"] = df["city"].apply(len)
# print(df.head)

# користувачі з доменом gmail.com
df["is_gmail"] = [True if "@gmail.com" in str(s).lower() else False for s in df["email"]]
# print(df.head)


# 4. Фільтрація даних

print("- користувачі з доменом **gmail.com**")
# Фільтрація користувачів, які мають Gmail-пошту
gmail_user = df.loc[df["is_gmail"] == True].copy()
# print(gmail_user)
# print("Gmail users:", len(gmail_user))

print(" Фільтрація за компаніями LLC або Ltd -----")
# Створюємо маску: перевіряємо, чи містить назва компанії слова LLC або LTD 
# у будь-якому регістрі (великі/малі літери).
mask_LLC_Ltd = df["company_name"].str.contains(
    r"\b(LLC|LLc|Llc|llc|LTD|LTd|Ltd|ltd)\b",    # патерн для пошуку
    regex=True,                                 # використовуємо регулярні вирази
    na=False                                    # якщо значення NaN — вважаємо False
)
# Застосовуємо маску до датафрейма та створюємо підвибірку компаній типу LLC/Ltd
company_LLC_Ltd = df.loc[mask_LLC_Ltd].copy()
# print(company_LLC_Ltd)
# print("Company LLC and Ltd:", len(company_LLC_Ltd))

print("- люди з міста **London** v")
people_London = df["city"].str.contains("London")


print('- компанії з назвою ≥ 4 слів')
# Рахуємо кількість слів у назві компанії
word_count = df["company_name"].str.split().str.len()

# Фільтруємо назви, де слів 4 або більше
companies_4_words = df[word_count >= 4].copy()
print(f'В назві 4 слова {companies_4_words}')



### **5. Позиційна вибірка (iloc)**
print("- Перші 10 рядків + колонки 2–5")
print(df.iloc[0:10, 2:5])
print("-  Кожний 10-й рядок  ")
print(df.iloc[::10])
print("- 5 випадкових рядків ")
print(df.sample(5, random_state=42))

# ***6. Групування та статистика**
# 6. Групування та статистика
# кількість людей у кожному місті
print(df["city"].value_counts())
# ТОП-5 міст
print(df["city"].value_counts().head(5))
# ТОП-5 email-доменів
print(df["email"].str.split("@").str[-1].value_counts().head(5))

# кількість унікальних доменів


df["domain"] = df["email"].str.split("@").str[-1]

abb_by_city = df.groupby("city").agg(
    people_count=("first_name", "count"), #створюємо стовбчик і потім кажемо, що чим наповнили: підрахунком імен
    uniq_dom=("domain", "nunique")
).sort_values("people_count", ascending=False).head(10)

print(abb_by_city)
count_by_city = df.groupby('city').size().reset_index(name='count')
print(count_by_city)

