import streamlit as st
import pandas as pd
print(1, st.session_state)
@st.dialog('По указанным критериям ничего не найдено')
def not_found_filter():
    st.query_params.clear()
    if st.button('Принять', key='empty_table'):
        st.session_state.clean_flag = True
def df_filter(df, key=None, value=None):
    if key and value:
        if key == 'find':
            if len(df[df.eq(value).any(axis=1)]):
                return df[df.eq(value).any(axis=1)]
            else:
                not_found_filter()
        elif len(df.loc[df[key] == value]):
            return df.loc[df[key] == value]
        else:
            not_found_filter()

    else:
        return df

keys_qp = {
    'stations':'Станция',
    'name':'Название',
    'owner':'Владелец',
    'type':'Тип коннектора',
    'status_st':'Статус',
    'status_con':'Статус',
    'metrick':'Показатели'
}

filter_names = ['status_st','owner']

df_connectors = pd.read_excel('db_connectors.xlsx')
df_stations = pd.read_excel('db_stations.xlsx')
usr = "Замарашко Р.Н."
st.html('nav_bar.html')

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = True
if 'clean_flag' not in st.session_state:
    st.session_state.clean_flag = False

if st.session_state.clean_flag:
    st.session_state.clean_flag = False
    st.query_params.clear()
    st.session_state['owner'] = 'Все'
    st.session_state['status_st'] = 'Все'
    if 'search_input' in st.session_state:
        if st.session_state.search_input:
            st.session_state.search_input = None
    for i in range(len(df_stations)):
        st.session_state[f'station_choose_button_{i}'] = False


b_st = st.session_state.sidebar_state
sidebar, main_ = st.columns([1, (4 if b_st else 6)])
sb = sidebar.container(border=b_st)
menu_switch = sb.button(("<< Hide menu" if b_st else "Open menu >>"), use_container_width=b_st)
if menu_switch:
    st.session_state.sidebar_state = not b_st
    st.rerun()

main_find_col, _ = main_.columns([2, 7])

    

#Выбор боковых фильтров
if b_st:
    if sb.button('Сбросить фильтры'):
        st.query_params.clear()
        st.session_state.clean_flag = True
        st.rerun()
    if sb.radio('По Владельцам', ['Все']+sorted(list(set(df_stations['Владелец']))), key='owner') != 'Все':
        st.query_params['owner']=st.session_state.owner
    else:
        if 'owner' in st.query_params:    
            del st.query_params['owner'] 
    if sb.radio('По статусам', ['Все']+sorted(list(set(df_stations['Статус']))), key='status_st') != 'Все':
        st.query_params['status_st']=st.session_state.status_st
    else:
        if 'status_st' in st.query_params:
            del st.query_params['status_st'] 


db_search = main_find_col.text_input('Введите значение:', placeholder='Поиск...', key='search_input')
if db_search:
    st.query_params["find"] = db_search



for key, value in st.query_params.items():
    df_stations = df_filter(df_stations, key=(keys_qp[key] if key in keys_qp else key), value=value)

main_.title('Станции')
if 'owner' in st.query_params:
    main_.write(f"По владельцам -> {st.query_params['owner']}")
if 'status_st' in st.query_params:
    main_.write(f"По статусу -> {st.query_params['status_st']}")


col_names = ['Станция','Название/Тип','Владелец','Статус','Показатели','Быстрые действия',]
iter_col = [station_col, name_type_col, owner_col, status_col, values_col, action_col] = main_.columns([1, 1, 1, 1, 2, 2]) 
for index_col, col_name in enumerate(col_names):
    iter_col[index_col].write(col_name)
try:
    if df_stations == None:
        not_found_filter()
except:
    for index_row, row in df_stations.iterrows():
        container_station = main_.container(border=True)
        iter_col = [station_col, name_type_col, owner_col, status_col, values_col, action_col] = container_station.columns([1, 1, 1, 1, 2, 2])
        for index_col, col_name in enumerate(col_names):
            if col_name == 'Станция':
                iter_col[index_col].checkbox(row[col_name], key=f"station_choose_button_{index_row}")  
            elif col_name == 'Быстрые действия':
                iter_col[index_col].pills('station_button_quick_action',['🗨️','🔄','🔲','🖥️','📖','⚙️'], key=f'station_button_quick_action_{index_row}', label_visibility='hidden')
            else:
                iter_col[index_col].write(row[col_name])
        if st.session_state[f"station_choose_button_{index_row}"]:
            df = df_connectors.loc[(df_connectors['Станция'] == df_stations['Станция'][index_row]) & (df_connectors['Владелец'] == df_stations['Владелец'][index_row])]
            container_connector_out = main_.container(border=True)
            for index_row_ext, row_ext in df.iterrows():
                container_connector_in = container_connector_out.container()
                iter_col = [station_col, name_type_col, owner_col, status_col, values_col, action_col] = container_connector_in.columns([1, 1, 1, 1, 2, 2])
                for index_col_ext, col_name_ext in enumerate(col_names):
                    
                    if col_name_ext == 'Быстрые действия':
                       print(f'connector_button_quick_action_{index_row}_{index_row_ext}')
                       iter_col[index_col_ext].pills(row_ext['Название/Тип'],['🗨️','▶️','↗️'], key=f'connector_button_quick_action_{index_row}_{index_row_ext}')
                    elif index_col_ext:
                        iter_col[index_col_ext].write(row_ext[col_name_ext])
                    else:
                        iter_col[index_col_ext].write(index_row_ext-index_row*3+1)
