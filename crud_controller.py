import psycopg
import uuid
import random
#from pprint import pprint

# TEST
prod_test = {'products': [{'Amount': 3.12, 'Product Name': 'VAHM - NOVA MOROA'},
              {'Amount': 3.98, 'Product Name': 'LO DE ME OCES -'},
              {'Amount': 3.14, 'Product Name': 'KUMBERLEY - KALEN - BXE'},
              {'Amount': 3.1, 'Product Name': 'HAYRETTIN TASKAVA - KANI'},
              {'Amount': 3.37, 'Product Name': 'BENIMLE MAYBOLUN - KANI'},
              {'Amount': 4.21, 'Product Name': 'YOGUNLUK VE AGRILAR - KANI'},
              {'Amount': 4.07, 'Product Name': 'BOS SNACK -'},
              {'Amount': 4.24, 'Product Name': 'EL ACARHI - CEYLAN EREM'},
              {'Amount': 4.12, 'Product Name': 'ANHARA JOA BIRI VAR - CAN'},
              {'Amount': 3.48, 'Product Name': 'CIKTIM BI YOLA - NOVA'},
              {'Amount': 3.05, 'Product Name': 'GUNCOR -'},
              {'Amount': 3.52, 'Product Name': 'KAZAZ -'},
              {'Amount': 3.1, 'Product Name': 'INCHIZE CAURA - CAN'}]}

# GLOBALS
host = "X"
port = "X"
dbname = "X"
user = "X"
password = "X"


"""
BAD APPROACH, BUT WE NEEDED TO BE FAST.
conn is a psycopg connection object that will
be declared and initialized globally to be used
under every CRUD method.
"""
conn = psycopg.connect(host=host,
                       port=port,
                       dbname=dbname,
                       user=user,
                       password=password)
cur = conn.cursor()


# HELPER METHODS
def show_users():
    cur.execute(
        "SELECT * FROM users"
    )
    test_dict: dict = {}
    swap_list = []
    for data in cur.fetchall():
        #pprint(data)
        print(data[0])
        swap_list.append({"a":data[0],
                          "b":data[1],
                          "c":data[2]})
        # for row in data:
        #     pprint(row)
    #pprint(swap_list)


def show_bills():
    cur.execute(
        "SELECT * FROM bills"
    )
    for data in cur.fetchall():
        print(data)

def show_products():
    cur.execute(
        "SELECT * FROM products"
    )
    for product in cur.fetchall():
        print(product)



def delete_all_bills():
    try:
        cur = conn.cursor()
        delete_query = """
        DELETE FROM bills
        """
        cur.execute(delete_query)
        conn.commit()

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print(f"An error occurred: {e}")










# CRUD METHODS
# Checks if the user exists.
def user_exist(user_mail: str) -> bool:
    query: str = f"SELECT EXISTS (SELECT 1 FROM users WHERE user_mail = %s);"
    cur.execute(query, 
                (user_mail, ))
    # for ans in cur.fetchall():
    #     return ans[]
    ans = cur.fetchone()
    return ans[0]


def create_user(user_mail: str,
                user_uid: str):
    query: str = """
        INSERT INTO users (user_mail, user_uuid)
        VALUES (%s, %s)
        """
    cur.execute(query,
                (user_mail, user_uid))
    conn.commit()
    


def create_bill(user_mail: str,
                products: dict) -> str:
    bill_uuid = str(uuid.uuid4())
    total_price = sum(float(product['Amount']) for product in products['products'])
    insert_query = """
        INSERT INTO bills (bill_uuid, bill_ref, bill_total)
        VALUES (%s, %s, %s)
        """
    cur.execute(insert_query,
                (bill_uuid, user_mail, total_price))
    conn.commit()

    insert_products(bill_uuid,
                    products)




def insert_products(bill_uuid, 
                    products):
    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Define the SQL query to insert a new product
        insert_query = """
        INSERT INTO products (bill_ref, product_name, product_price)
        VALUES (%s, %s, %s)
        """

        # Execute the query for each product in the JSON
        for product in products['products']:
            product_name = product['Product Name']
            product_price = float(product['Amount'])

            cur.execute(insert_query, (bill_uuid, product_name, product_price))

        conn.commit()

        print("Products inserted successfully.")

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print(f"An error occurred: {e}")



def get_all_bills_with_products(user_email):
    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Define the SQL query to retrieve all bills and their products for a given user email
        select_query = """
        SELECT b.bill_uuid, p.product_name, p.product_price
        FROM bills b
        JOIN products p ON b.bill_uuid = p.bill_ref
        WHERE b.bill_ref = (
            SELECT user_mail
            FROM users
            WHERE user_mail = %s
        )
        """

        # Execute the query with the provided user email
        cur.execute(select_query, (user_email,))

        # Fetch all rows from the result
        rows = cur.fetchall()

        # Create a dictionary to store the results
        total_bills = []
        current_bill = {}
        current_products = []

        # Iterate over the rows and format the results
        for row in rows:
            bill_uuid, product_name, product_price = row

            # If the bill changes, add the current products to the total bills list
            if not current_bill or current_bill['bill_uuid'] != bill_uuid:
                if current_bill:
                    total_bills.append({'products': current_products})
                current_bill = {'bill_uuid': bill_uuid}
                current_products = []

            # Assign the value of "IsLoss" randomly
            is_loss = random.choice(['true', 'false'])

            # Add the current product to the list of products for the current bill
            current_products.append({
                'Product Name': product_name,
                'Amount': str(product_price),
                'IsLoss': is_loss
            })

        # Add the products of the last bill to the total bills list
        if current_products:
            total_bills.append({'products': current_products})

        return {'totalBills': total_bills}

    except Exception as e:
        print(f"An error occurred: {e}")