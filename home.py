import streamlit as st
from function import insert_user, nav_page, get_users, stylus, session_declare, insert_order, get_product, captilize
import io
from PIL import Image
import time

stylus()

session_declare()

captilize()

if st.session_state.user_id is not None:
    logintxt = "Logout"
    signuptxt = "Profile"
else:
    logintxt = "Login"
    signuptxt = "Signup"


tabl,  tab3, tab4, tab5, tab6 = st.tabs(["Home", "Shop","Contact Us", logintxt, signuptxt])
with tabl:
    row2col1, row2col2 = st.columns([0.5, 0.5])
    with row2col1:
        st.title('Coffee Shop')
        st.write("Welcome to our cozy coffee haven! Indulge in rich aromas, crafted beverages, and delightful treats at our friendly café. Whether you're seeking a tranquil moment or a vibrant social hub, our coffeehouse offers the perfect blend of comfort and community. Join us for a sip of warmth and a taste of relaxation.")
    with row2col2:
        st.image('images/test.jpg')

    st.markdown(f'''
        <div style="height:50px;"></div>''',
        unsafe_allow_html=True,
    )

    row3col1 = st.columns([1])
    st.write('Hello world')


with tab3:
    products = get_product()

    #` Calculate number of rows
    num_rows = len(products) // 3 + (1 if len(products) % 3 != 0 else 0)

    # Generate dynamic layout
    for row in range(num_rows):
        col1, col2, col3 = st.columns(3)  # Create 3 columns for each row
        for idx in range(3):
            product_idx = row * 3 + idx
            if product_idx < len(products):
                with eval(f"col{idx+1}"):  # Evaluate the appropriate column
                    image_bytes = products[product_idx][3]
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="", use_column_width=True)
                    st.write(products[product_idx][1])
                    st.write(f"Price: ${products[product_idx][2]}")
                    order = st.button('Order Now', key=product_idx)

                    if order:
                        if st.session_state.user_id is not None:
                            insert_order(products[product_idx][1],products[product_idx][2],st.session_state.user_id)
                        else:
                            st.error('not login')
                            nav_page('login')
with tab4:
    # st.write('this is contact us page')
    st.markdown('''
                <style>
                #my-image {
        width: 300px;
        height: 300px;
        border-radius: 150px;
}
                </style>
''', unsafe_allow_html=True)
    col5 , col6 = st.columns([0.5,0.5])
    # col5 , col6 = st.columns([5,5])
    col5.markdown('''
                  # Anish Maka <br>
                  +977 9860406626<br>
                  https://github.com/YoG-Anish<br>
                  :cop:https://www.facebook.com/anish.maka.9/<br>
                  Location : Milanchowk, Bhaktapur<br>
                  ''', unsafe_allow_html=True)

    col6.markdown('<img id="my-image" src="https://i.imgur.com/IzaoSYT.jpeg" alt="My Image">', unsafe_allow_html=True)
    # col5.markdown('<img id="my-image" src="./images/anishsq.jpg" alt="My Image">', unsafe_allow_html=True)
    # col7.image('./images/anishsq.jpg', width = 300)
with tab5:
    if st.session_state.user_id is None:
        with st.form('loginform',clear_on_submit=False):
            username = st.text_input(' ', placeholder='Username', max_chars=60)
            password = st.text_input(' ', placeholder='Password', type="password")
            login_button = st.form_submit_button('Submit')

        if login_button:
            corflag = 0
            user_id=0
            user_role = 0
            users = get_users()
            for x in users:
                if username == x[1] and password == x[2]:
                    user_id = x[0]
                    user_role = x[4]
                    corflag = 1

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
        lgout = st.button('Log Out')
        if lgout:
            st.write('<meta http-equiv="refresh" content="0; URL=/" />', unsafe_allow_html=True)

with tab6:
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
        cur_user = get_users()
        if cur_user[0][4] == 1:
            role = "Admin"
        else:
            role = "Customer"
        st.write("User ID: #" + str(cur_user[0][0]))
        st.write("Name: " + cur_user[0][1])
        st.write("Email: " + cur_user[0][3])
        st.write("Role: " + role)
