import streamlit as st
import pandas as pd
from datetime import datetime

def df_redactor(df):
    df['Создатель'].loc[df['Создатель'] == usr] = 'Я'
    df['Исполнитель'].loc[df['Исполнитель'] == usr] = 'Я'
@st.dialog('По указанным критериям ничего не найдено')
def not_found_filter():
    st.query_params.clear()
    if st.button('Принять', key='empty_table'):
        st.session_state.clean_flag = True
        st.rerun()
def df_filter(df, key=None, value=None):
    if key and value:
        if key == 'find':
            if len(df[df.eq(value).any(1)]):
                return df[df.eq(value).any(1)]
            else:
                not_found_filter()
        elif len(df.loc[df[key] == value]):
            return df.loc[df[key] == value]
        else:
            not_found_filter()

    else:
        return df

keys_qp = {
    'creator':'Создатель',
    'executer':'Исполнитель',
    'date':'Дата',
    'stations':'Станция',
    'host':'Владелец',
    'type':'Тип заявки',
    'status':'Статус'
}

df = pd.read_excel('db_applications.xlsx')
df['Дата'] = df['Дата'].astype('datetime64[ns]')
st.html('nav_bar.html')
filter_names = ['date','stations','host','type','status']

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = True
if 'clean_flag' not in st.session_state:
    st.session_state.clean_flag = False
usr = "Замарашко Р.Н."

b_st = st.session_state.sidebar_state
sidebar, main_ = st.columns([1, (4 if b_st else 6)])
sb = sidebar.container(border=b_st)
menu_switch = sb.button(("<< Hide menu" if b_st else "Open menu >>"), use_container_width=b_st)

main_find, _ = main_.columns([1,7])
if 'search_input' in st.session_state and st.session_state.clean_flag:
    st.session_state.clean_flag = False
    st.query_params.clear()
    if st.session_state.search_input:
        st.session_state.search_input = None
    for i in filter_names:
        if i != 'date':
            st.session_state[i]='-'
        else:
            st.session_state[i] = df['Дата'].min(), df['Дата'].max()

db_search = main_find.text_input('Введите значение:', placeholder='Поиск...', key='search_input')


if db_search:
    st.query_params["find"] = db_search
main_.title('Заявки -> Все', anchor=False)
df_redactor(df)

if menu_switch:
    st.session_state.sidebar_state = not b_st
if b_st:
    if sb.button('Все', use_container_width=True):
        st.query_params.clear()
        st.session_state.clean_flag = True
    if sb.button('Созданные мной', use_container_width=True):
        st.query_params.clear()
        st.query_params['creator'] = 'Я'
    if sb.button('Я исполнитель', use_container_width=True):
        st.query_params.clear()
        st.query_params['executer'] = 'Я'

# for key, value in st.query_params.items():
#     df = df_filter(df, key=(keys_qp[key] if key in keys_qp else key), value=value)



filter_container = main_.container(border=True)
filter_container.write('Выбрать фильтр:')
date_col, station_col, host_col, type_col, status_col, _ = filter_container.columns([2,1,1,1,1,2])
filter_params = [
    date_col.date_input('Дата', [df['Дата'].min(),df['Дата'].max()],format="YYYY-MM-DD", key=filter_names[0]),
    station_col.selectbox('Станция',sorted(list(set(['-'] + df['Станция'].to_list()))), key=filter_names[1]),
    host_col.selectbox('Владелец',sorted(list(set(['-'] + df['Владелец'].to_list()))), key=filter_names[2]),
    type_col.selectbox('Тип',sorted(list(set(['-'] + df['Тип заявки'].to_list()))), key=filter_names[3]),
    status_col.selectbox('Статус',sorted(list(set(['-'] + df['Статус'].to_list()))), key=filter_names[4]),
]

for index, f in enumerate(filter_params):
    if f != '-' and filter_names[index] != 'date':
        st.query_params[filter_names[index]] = f
    else:
        if filter_names[index] in st.query_params:
            del st.query_params[filter_names[index]]



    # if filter_container.button('Принять', key='filter_accept'):
for key, value in st.query_params.items():
    df = df_filter(df, key=(keys_qp[key] if key in keys_qp else key), value=value)
if filter_container.button('Сбросить', key='filter_cleaner'):
    st.session_state.clean_flag = True
    st.rerun()
try:
    if len(df):
        main_.dataframe(df, use_container_width=True)
except:
    pass