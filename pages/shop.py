import streamlit as st
from function import get_product, stylus, session_declare, nav_page, insert_order, captilize
from PIL import Image
import io

stylus()

st.title('Shop')

session_declare()
captilize()
products = get_product()

# Calculate number of rows
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
                quantity = st.number_input('Quantity', max_value=5, min_value=1, key=str(product_idx) + 'q')
                order = st.button('Order Now', key=product_idx)

                if order:
                    if st.session_state.user_id is not None:
                        insert_order(products[product_idx][1],products[product_idx][2],st.session_state.user_id, quantity)
                        st.success('order is placed. Please pickup your order at the shop')
                    else:
                        st.error('not login')
                        nav_page('login')
                        # st.write('<meta http-equiv="refresh" content="0; URL=/?tab=login" />', unsafe_allow_html=True)
                        # nav_page('home')
                        # st.query_params(tab="login")
# count = 0

# for x in products:
#     product_name = x[1]
#     product_price = x[2]
#     count+=1
#     if count % 3==0:
#         print("new row")
#     image_bytes = x[3]
#     image = Image.open(io.BytesIO(image_bytes))
#     st.image(image, caption="", use_column_width=True)
#     st.write(f"Product Name: {x[1]}")  
#     st.write(f"Price: ${x[2]}")
#     order = st.button('Order Now', key=count)
#     if order:
#         st.write(product_name)
#         st.write(product_price)