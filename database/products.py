import sqlite3
from sqlite3 import Error
from venv import create

from .connection import create_connection

def insert_products(data):
    conn = create_connection()

    sql = """ INSERT INTO products( name_pro, price, create_date)
            VALUES(?,?,?)
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error at insert_products() : {str(e)}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def select_products_by_id(_id):
    conn = create_connection()
    sql = f" SELECT * FROM products WHERE id = {_id}"
    
    try: 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        product = dict(cur.fetchone())
        return product
    except Error as e:
        print(f" Error in select_products_by_id(): {str(e)}")
    finally:
        cur.close()
        conn.close()

def select_all_products():
    conn = create_connection()
    sql = "SELECT * FROM products"

    try:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        product_rows = cur.fetchall()
        products = [dict(row) for row in product_rows]
        return products

    except Error as e:
        print(f" Error in select_all_products(): {str(e)}")
    finally:
        cur.close()
        conn.close()

def edit_product(_id, data):
    conn = create_connection()
    sql = f"UPDATE products SET name_pro = ?, price = ? WHERE id = {_id}"

    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        return True
    except Error as e:
        print(f"Error at edit_product_by_id() : {str(e)}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_product(_id):
    conn = create_connection()
    sql = f"""DELETE FROM products WHERE id = {_id}"""

    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return True
    except Error as e:
        print(f"Error at delete_product() : {str(e)}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()