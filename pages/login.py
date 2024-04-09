import streamlit as st
from function import nav_page, get_users, session_declare, captilize
import time

session_declare()
captilize()
if st.session_state.user_id is None:
    st.title('Login')
    with st.form('loginform',clear_on_submit=False):
            username = st.text_input(' ', placeholder='Username', max_chars=60)
            password = st.text_input(' ', placeholder='Password', type="password")
            login_button = st.form_submit_button('Submit')

    if login_button:
        corflag = 0
        user_role = 0
        user_id = 0
        users = get_users()
        for x in users:
            if username == x[1] and password == x[2]:
                user_id = x[0]
                corflag = 1
                user_role = x[4]

        if corflag:
            st.success('login success')
            time.sleep(1)
            print(user_id)
            print(user_role)
            st.session_state.user_id = user_id
            st.session_state.user_role = user_role
            nav_page("shop")
        else:
            st.write('login abort')
else:
    st.write('You are logged in. Click on the button below to log out')
    lgout = st.button('Log Out')
    if lgout:
        st.write('<meta http-equiv="refresh" content="0; URL=/" />', unsafe_allow_html=True)