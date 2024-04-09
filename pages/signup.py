
import streamlit as st
from function import insert_user, nav_page, session_declare, captilize
import time

session_declare()
captilize()
if st.session_state.user_id is None:
    with st.form('signupform',clear_on_submit=False):
            st.write("<h2>Sign Up</h2>", unsafe_allow_html=True)
            username = st.text_input(' ', placeholder='User Name', max_chars=20 )
            email = st.text_input(' ', placeholder='Email', max_chars=80)
            password = st.text_input(' ', placeholder='Password', type="password")
            signuped = st.form_submit_button('Submit')

    if signuped:
        if(len(email)==0 or len(password)==0 or len(username)==0):
            if len(email)==0:
                st.error('Email field is empty')
            if len(password)==0:
                st.error('Password field is empty')
            if len(username)==0:
                st.error('Username field is empty')
        else:
            insert_user(username, password, email, 2)
            st.success("Signup successful, you can now login")
            time.sleep(1)
            nav_page("shop")
else:
    st.write('You are logged in. Click on the button below to log out')
    lgout = st.button('Log Out')
    if lgout:
        st.write('<meta http-equiv="refresh" content="0; URL=/" />', unsafe_allow_html=True)