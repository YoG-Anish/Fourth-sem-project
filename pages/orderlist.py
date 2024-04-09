import streamlit as st
from function import get_order, nav_page, session_declare, captilize
import pandas as pd

session_declare()
captilize()
if st.session_state.user_id is None or st.session_state.user_role != 1:
    st.write("Sorry you don't have the authority to open this page. ")
    auth = st.button('Authorize')

    if auth:
        nav_page('login')
else:
        st.title('Order list')

        orders = get_order()
        order_id = []

        data = {'Order ID': ['#'+ str(x[0]) for x in orders],
                'Product Name': [x[1] for x in orders],
                'Product Price': ['Rs. '+ str(x[2]) for x in orders],
                'User ID': ['#'+ str(x[3]) for x in orders]}

        df = pd.DataFrame(data)
        df.index += 1
        st.table(df)


