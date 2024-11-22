import streamlit as st
st.html('nav_bar.html')

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = True


b_st = st.session_state.sidebar_state
sidebar, main_ = st.columns([1, (4 if b_st else 6)])
sb = sidebar.container(border=b_st)

menu_switch = sb.button(f'{("Hide" if b_st else "Open")} menu', use_container_width=b_st)
main_.title('Stats and Insights', anchor=False)
main_.image('main.png')
if menu_switch:
    st.session_state.sidebar_state = not b_st
    st.rerun()
if b_st:
    sb.image('sidebar.png', width=430)