import psycopg2
from config import load_config
from streamlit.components.v1 import html
import streamlit as st

def stylus():
    st.markdown(f"""
    <style>
        .block-container{{
            width: 1440px;
            max-width: 100%;
        }}
        #tabs-bui2-tabpanel-2{{
            max-width: 50%; 
        }}
    </style>""",
    unsafe_allow_html=True,
)
def captilize():
    st.markdown("""
    <style>
        div[data-testid="stSidebarNav"]{
            text-transform: capitalize;
        }
    </style>
    """, unsafe_allow_html=True)


def session_declare():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
        st.session_state.user_role = None

#db handler
def insert_user(username, password, email, userrole):
    sql = """INSERT INTO users(username, password, email, userrole)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    
    id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (username,password, email, userrole))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return id
    
def get_users():
    config  = load_config()
    userdata = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, password, email, userrole FROM users")
                # print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    userdata.append(row)
                    row = cur.fetchone()
                return userdata

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_product(product_name, product_price, product_image):
    sql = """INSERT INTO product(product_name, product_price, product_image)
             VALUES(%s, %s, %s) RETURNING product_id;"""
    
    product_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (product_name,product_price, product_image))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    product_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return product_id

def get_product():
    config  = load_config()
    productdata = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT product_id, product_name, product_price, product_image FROM product")
                # print("The number of parts: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    productdata.append(row)
                    row = cur.fetchone()
                return productdata

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_order(product_name, product_price, user_id, quantity):
    sql = """INSERT INTO orders(product_name, product_price, id, quantity)
             VALUES(%s, %s, %s, %s) RETURNING order_id;"""
    
    order_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (product_name,product_price, user_id, quantity))

                # get the generated id back                
                rows = cur.fetchone()
                if rows:
                    order_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        return order_id

def get_order():
    config  = load_config()
    orders = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT order_id, product_name, product_price, id FROM orders")
                row = cur.fetchone()

                while row is not None:
                    orders.append(row)
                    row = cur.fetchone()
                return orders

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#page navigation
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

