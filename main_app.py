import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image

# заголовок приложения
st.title('EDA банковских данных клиентов с таргетированной рекламой')

# грузим данные
df = pd.read_csv('union_data.csv')
df = df.drop('AGREEMENT_RK', axis = 1)

# Просмотр датасета
st.subheader("Первые 20 строчек датасета")
st.dataframe(df.head(20))

#распределение признаков
st.subheader("Распределение данных")
for i in df.columns:
    st.text(i)
    fig = px.box(df[i])
    st.plotly_chart(fig)

st.write('При изучении распределения признаков выявлены аномальные \
         (вбросовые) значения по нескольким признакам: \
         LOAN_NUM_CLOSED, PERSONAL_INCOME, LOAN_NUM_TOTAL, CHILD_TOTAL \
         DEPENDANTS.')


#Корреляция
st.subheader("Корреляция между признаками")
img = Image.open('corr_matrix.png')
st.image(img, width=1000)

st.write('Самые коррелирующие между собой признаки это AGE и SOCSTATUS_PENS_FL, \
         DEPENDANTS и CHILD_TOTAL. Отсутсвует корреляция между всеми параметрами и целевым значением TARGET.')


#зависимость признаков от целевой переменной
st.subheader("зависимость признаков от целевой переменной")
for i in df.columns:
    if i == 'TARGET':
        continue
    st.text(f"зависимость {i} от 'TARGET'")
    fig = px.scatter(df, y = i, x = 'TARGET')
    st.plotly_chart(fig)

st.write('Ввиду категориального значения целевой переменной TARGET \
         точечное распреедление параметров неинформативно отображается на точечном графике.')

# вычисление числовых характеристик распределения числовых столбцов (среднее, min, max, медиана и так далее)
st.subheader("Подробное изучения числовых характеристик")
st.dataframe(df.describe())

# распределение значений в TARGET
st.subheader("Распределение значений в TARGET")

target_values = list(df['TARGET'])
count_1 = target_values.count(1)
count_0 = target_values.count(0)

st.text(f'Количество объектов класса 0 = {count_0}')
st.text(f'Количество объектов класса 1 = {count_1}')

fig = px.bar([count_0, count_1])
st.plotly_chart(fig)

st.write('Обнаружен существенный дисбаланс классов.')

# Изучения кол-ва кредитов в зависимости от групп
st.subheader("Изучения кол-ва кредитов в зависимости от групп")

st.write('Была добавлена новая колонка PERSONAL_INCOME_GR с делением на группы в зависимости от дохода')

df['PERSONAL_INCOME_GR'] = 'Nan'
for i in df.index:
    if df['PERSONAL_INCOME'][i] <= 10000:
        df['PERSONAL_INCOME_GR'][i] = 'C'
    if df['PERSONAL_INCOME'][i] >= 10000 and df['PERSONAL_INCOME'][i] <= 17000:
        df['PERSONAL_INCOME_GR'][i] = 'B' 
    if df['PERSONAL_INCOME'][i] >= 17000:
        df['PERSONAL_INCOME_GR'][i] = 'A' 

def plotly_ch(option_1):
    '''отображение графиков'''
    st.write(f'Кол-во кредитов (ВСЕГО) по группам {option_1}')
    df_pl = df.groupby(option_1)['LOAN_NUM_TOTAL'].sum()
    fig1 = px.bar(df_pl)
    st.plotly_chart(fig1)

    st.write(f'Кол-во закрытых кредитов по группам {option_1}')
    df_pl = df.groupby(option_1)['LOAN_NUM_CLOSED'].sum()
    fig2 = px.bar(df_pl)
    st.plotly_chart(fig2)
    

def show_list():
    '''Получение параметров для графика'''
    st.write('Выберите опцию:')
    option_1 = st.selectbox(
     'Выбирите параметр для исследования на кол-во кредитов и их возврат',
     ('AGE', 'GENDER', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 
      'PERSONAL_INCOME_GR', 'CHILD_TOTAL', 'DEPENDANTS'))

    return option_1

# рисуем график
option_1 = show_list()
plotly_ch(option_1)