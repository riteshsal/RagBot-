import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    st.sidebar.header("Upload PDFs")
    uploaded_files=st.sidebar.file_uploader("upload multiple PDFs",type="pdf", accept_multiple_files=True)
    if st.sidebar.button("Upload to DB") and uploaded_files:
        response=upload_pdfs_api(uploaded_files)
        if response.status_code==200:
            st.sidebar.success("Uploaded succesfully")
        else:
            st.sidebar.error(f"Error: {response.text}")