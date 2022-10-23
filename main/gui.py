import streamlit as st

my_page = st.sidebar.radio('Page Navigation', ['Scrape KIID', 'KIID visualization'])
if my_page == 'Scrape KIID':
    st.title('Scrape KIID')
    URL = st.text_input("URL")
    Destination = st.text_input("Destination")
    start = st.button("Start")
    if start:
        st.text("Scraping data...")
        stop = st.button("Stop")
        if stop:
            # wyłączyć scrapera
            pass
else:
    st.title('KIID visualization')
    file = st.file_uploader("Upload KIDD")
    visualize = st.checkbox("Visualize")
    if visualize:
        st.header("Bag of words")
        st.dataframe()
        bow = st.button("Download bag of words")
        if bow:
            pass
        st.header("Required phrases")
        st.dataframe()
        rp = st.button("Download required phrases")
        if rp:
            pass
        st.header("Data")
        st.dataframe()
        dt = st.button("Download data")
        if dt:
            pass
