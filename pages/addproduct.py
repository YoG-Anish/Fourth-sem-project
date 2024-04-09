import streamlit as st
from function import insert_product, session_declare, nav_page, captilize
import psycopg2

session_declare()
captilize()
if st.session_state.user_id is None or st.session_state.user_role != 1:
    st.write("Sorry you don't have the authority to open this page. ")
    auth = st.button('Authorize')

    if auth:
        nav_page('login')
else:
    with st.form('addproduct',clear_on_submit=False):
        st.write("<h2>Add Product</h2>", unsafe_allow_html=True)
        product_name = st.text_input(' ', placeholder='Product Name', max_chars=20 )
        product_price = st.text_input(' ', placeholder='Price', max_chars=80)

        uploaded_file = st.file_uploader("Upload Product Image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        addproduct = st.form_submit_button('Submit')

    if addproduct:
        image_bytes = uploaded_file.getvalue()
        insert_product(product_name, product_price, psycopg2.Binary(image_bytes))
        print('product inserted')
        nav_page('shop')
