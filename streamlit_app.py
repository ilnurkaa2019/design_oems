import streamlit as st
st.set_page_config(layout="wide")
def main():

    applications_page = st.Page(
        'admin/applications.py',
        title="Заявки",
        url_path="/applications",
        default=False
    )
    dashboard_page = st.Page(
        'admin/dashboard.py',
        title="Дашборд",
        url_path="/dashboard",
        default=False
    )
    stations_page = st.Page(
        'admin/stations.py',
        title="Станции",
        url_path="/stations",
        default=False
    )
    page_list = [dashboard_page, applications_page, stations_page]
    pg = st.navigation(page_list, position="hidden")
    pg.run()
if __name__ == "__main__":
    main()
